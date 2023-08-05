"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from aiomisc.service.aiohttp import (
    AIOHTTPService,
)

from minos.common import (
    MinosConfig,
)

from .builders import (
    RestBuilder,
)


class RestService(AIOHTTPService):
    """
    Rest Interface

    Expose REST Interface handler using aiomisc AIOHTTPService.

    """

    def __init__(self, config: MinosConfig, **kwargs):
        address = config.rest.broker.host
        port = config.rest.broker.port
        super().__init__(address=address, port=port, **kwargs)
        self.rest = RestBuilder.from_config(config=config, **kwargs)

    async def create_application(self):
        return self.rest.get_app()  # pragma: no cover
