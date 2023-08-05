# Copyright (C) 2020 Clariteia SL
#
# This file is part of minos framework.
#
# Minos framework can not be copied and/or distributed without the express
# permission of Clariteia SL.

from __future__ import (
    annotations,
)

import logging
from abc import (
    abstractmethod,
)
from datetime import (
    datetime,
)
from inspect import (
    isclass,
)
from typing import (
    Any,
    Callable,
    NoReturn,
)

from minos.common import (
    MinosModel,
    import_module,
)

from ...exceptions import (
    MinosNetworkException,
)
from ..entries import (
    HandlerEntry,
)
from .setups import (
    HandlerSetup,
)

logger = logging.getLogger(__name__)


class Handler(HandlerSetup):
    """
    Event Handler

    """

    __slots__ = "_handlers", "_handlers"

    def __init__(self, *, records: int, handlers: dict[str, dict[str, Any]], **kwargs: Any):
        super().__init__(**kwargs)
        self._handlers = handlers
        self._records = records
        self._retry = kwargs.get("retry")

    async def dispatch(self) -> NoReturn:
        """Event Queue Checker and dispatcher.

        It is in charge of querying the database and calling the action according to the topic.

            1. Get periodically 10 records (or as many as defined in config > queue > records).
            2. Instantiate the action (asynchronous) by passing it the model.
            3. If the invoked function terminates successfully, remove the event from the database.

        Raises:
            Exception: An error occurred inserting record.
        """

        pool = await self.pool
        with await pool.cursor() as cursor:
            # aiopg works in autocommit mode, meaning that you have to use transaction in manual mode.
            # Read more details: https://aiopg.readthedocs.io/en/stable/core.html#transactions.
            await cursor.execute("BEGIN")

            # Select records and lock them FOR UPDATE
            await cursor.execute(_SELECT_NON_PROCESSED_ROWS_QUERY % (self.TABLE_NAME, self._retry, self._records),)
            result = await cursor.fetchall()

            for row in result:
                dispatched = False
                try:
                    await self.dispatch_one(row)
                    dispatched = True
                except Exception as exc:
                    logger.warning(f"Raised an exception while dispatching a message: {exc!r}")
                finally:
                    if dispatched:
                        await cursor.execute(_DELETE_PROCESSED_QUERY % (self.TABLE_NAME, row[0]))
                    else:
                        await cursor.execute(_UPDATE_NON_PROCESSED_QUERY % (self.TABLE_NAME, row[0]))

            # Manually commit
            await cursor.execute("COMMIT")

    async def dispatch_one(self, row: tuple[int, str, int, bytes, datetime]) -> NoReturn:
        """Dispatch one row.

        :param row: Row to be dispatched.
        :return: This method does not return anything.
        """
        id = row[0]
        topic = row[1]
        callback = self.get_action(row[1])
        partition_id = row[2]
        data = self._build_data(row[3])
        retry = row[4]
        created_at = row[5]

        entry = HandlerEntry(id, topic, callback, partition_id, data, retry, created_at)

        await self._dispatch_one(entry)

    def get_action(self, topic: str) -> Callable:
        """Get Event instance to call.

        Gets the instance of the class and method to call.

        Args:
            topic: Kafka topic. Example: "TicketAdded"

        Raises:
            MinosNetworkException: topic TicketAdded have no controller/action configured, please review th
                configuration file.
        """
        if topic not in self._handlers:
            raise MinosNetworkException(
                f"topic {topic} have no controller/action configured, " f"please review th configuration file"
            )

        event = self._handlers[topic]

        controller = import_module(event["controller"])
        if isclass(controller):
            controller = controller()
        action = getattr(controller, event["action"])

        logger.debug(f"Loaded {action!r} action!")
        return action

    @abstractmethod
    def _build_data(self, value: bytes) -> MinosModel:
        raise NotImplementedError

    @abstractmethod
    async def _dispatch_one(self, row: HandlerEntry) -> NoReturn:
        raise NotImplementedError


_SELECT_NON_PROCESSED_ROWS_QUERY = """
SELECT *
FROM %s
WHERE retry <= %d
ORDER BY creation_date
LIMIT %d
FOR UPDATE
SKIP LOCKED;
""".strip()

_DELETE_PROCESSED_QUERY = """
DELETE FROM %s
WHERE id = %d;
""".strip()

_UPDATE_NON_PROCESSED_QUERY = """
UPDATE %s
    SET retry = retry + 1
WHERE id = %s;
""".strip()
