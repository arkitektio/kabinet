from graphql import OperationType
from pydantic import Field
from rath import rath
import contextvars
import logging

from rath.links.base import TerminatingLink
from rath.contrib.fakts.links.aiohttp import FaktsAIOHttpLink
from rath.contrib.fakts.links.subscription_transport_ws import FaktsWebsocketLink
from rath.contrib.herre.links.auth import HerreAuthLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.auth import AuthTokenLink

from rath.links.base import TerminatingLink
from rath.links.compose import compose
from rath.links.dictinglink import DictingLink
from rath.links.shrink import ShrinkingLink
from rath.links.split import SplitLink
from rath.links.websockets import WebSocketLink


current_kuay_rath = contextvars.ContextVar("current_kuay_rath")


class KuayRath(rath.Rath):
    link: TerminatingLink = Field(
        default_factory=lambda: compose(
            ShrinkingLink(),
            DictingLink(),
            HerreAuthLink(),
            FaktsAIOHttpLink(fakts_group="port"),
        )
    )

    async def __aenter__(self):
        current_kuay_rath.set(self)
        await super().__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        current_kuay_rath.set(None)
