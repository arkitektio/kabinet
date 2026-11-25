"""How ``Kabinet`` reaches a resolved deployment: its links."""

from arkitekt_spec.declare.wiring import Alias, TokenLoader
from fakts.contrib.rath.auth import FaktsAuthLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.graphql_ws import GraphQLWSLink
from rath.links.split import SplitLink

from graphql import OperationType
from kabinet.rath import KabinetLinkComposition, KabinetRath


def kabinet_rath(kabinet: Alias, tokens: TokenLoader) -> KabinetRath:
    """The rath over http and ws."""
    return KabinetRath(
        link=KabinetLinkComposition(
            auth=FaktsAuthLink(token_loader=tokens),
            split=SplitLink(
                left=AIOHttpLink(
                    endpoint_url=kabinet.to_http_path("graphql"),
                    proxy=kabinet.proxy,
                    ssl_context=kabinet.ssl_context(),
                ),
                right=GraphQLWSLink(
                    ws_endpoint_url=kabinet.to_ws_path("graphql"),
                    proxy=kabinet.proxy,
                    ssl_context=kabinet.ssl_context(),
                ),
                split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
            ),
        )
    )


__all__ = ["kabinet_rath"]
