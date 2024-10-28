from kabinet.kabinet import Kabinet
from kabinet.rath import KabinetLinkComposition, KabinetRath
from rath.links.split import SplitLink
from fakts_next.contrib.rath.aiohttp import FaktsAIOHttpLink
from fakts_next.contrib.rath.graphql_ws import FaktsGraphQLWSLink
from herre_next.contrib.rath.auth_link import HerreAuthLink
from graphql import OperationType
from herre_next import Herre
from fakts_next import Fakts

from arkitekt_next.base_models import Manifest

from arkitekt_next.service_registry import (
    Params,
)
from arkitekt_next.base_models import Requirement


def init_services(service_builder_registry):

    class ArkitektNextKabinet(Kabinet):
        rath: KabinetRath

    def build_arkitekt_next_fluss(
        fakts: Fakts, herre: Herre, params: Params, manifest: Manifest
    ):
        return ArkitektNextKabinet(
            rath=KabinetRath(
                link=KabinetLinkComposition(
                    auth=HerreAuthLink(herre=herre),
                    split=SplitLink(
                        left=FaktsAIOHttpLink(
                            fakts_group="kabinet", fakts=fakts, endpoint_url="FAKE_URL"
                        ),
                        right=FaktsGraphQLWSLink(
                            fakts_group="kabinet",
                            fakts=fakts,
                            ws_endpoint_url="FAKE_URL",
                        ),
                        split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                    ),
                )
            )
        )

    service_builder_registry.register(
        "kabinet",
        build_arkitekt_next_fluss,
        Requirement(
            key="kabinet",
            service="live.arkitekt.kabinet",
            description="An instance of ArkitektNext Kabinet to retrieve nodes from",
        ),
    )
