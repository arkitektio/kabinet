try:
    from .kabinet import Kabinet
    from .rath import KabinetLinkComposition, KabinetRath
    from rath.links.split import SplitLink
    from rath.contrib.fakts.links.aiohttp import FaktsAIOHttpLink
    from rath.contrib.fakts.links.graphql_ws import FaktsGraphQLWSLink
    from rath.contrib.herre.links.auth import HerreAuthLink
    from graphql import OperationType
    from herre import Herre
    from fakts import Fakts

    from arkitekt_next.service_registry import (
        get_default_service_builder_registry,
        Params,
    )
    from arkitekt_next.model import Requirement

    class ArkitektNextKabinet(Kabinet):
        rath: KabinetRath

    def build_arkitekt_next_fluss(fakts: Fakts, herre: Herre, params: Params):
        return ArkitektNextKabinet(
            rath=KabinetRath(
                link=KabinetLinkComposition(
                    auth=HerreAuthLink(herre=herre),
                    split=SplitLink(
                        left=FaktsAIOHttpLink(fakts_group="kabinet", fakts=fakts),
                        right=FaktsGraphQLWSLink(fakts_group="kabinet", fakts=fakts),
                        split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                    ),
                )
            )
        )

    service_builder_registry = get_default_service_builder_registry()
    service_builder_registry.register(
        "kabinet",
        build_arkitekt_next_fluss,
        Requirement(
            service="live.arkitekt.kabinet",
            description="An instance of ArkitektNext Kabinet to retrieve nodes from",
        ),
    )
    imported = True

    try:
        from rekuest_next.structures.default import (
            get_default_structure_registry,
            PortScope,
            id_shrink,
        )
        from rekuest_next.widgets import SearchWidget

        from kabinet.api.schema import (
            PodFragment,
            apod,
            DeploymentFragment,
            aget_deployment,
            ReleaseFragment,
            aget_release,
        )

        structure_reg = get_default_structure_registry()
        structure_reg.register_as_structure(
            PodFragment,
            identifier="@kabinet/pod",
            scope=PortScope.GLOBAL,
            aexpand=apod,
            ashrink=id_shrink,
        )
        structure_reg.register_as_structure(
            DeploymentFragment,
            identifier="@kabinet/deployment",
            scope=PortScope.GLOBAL,
            aexpand=aget_deployment,
            ashrink=id_shrink,
        )
        structure_reg.register_as_structure(
            ReleaseFragment,
            identifier="@kabinet/release",
            scope=PortScope.GLOBAL,
            aexpand=aget_release,
            ashrink=id_shrink,
        )

    except ImportError as e:
        raise e

except ImportError as e:
    imported = False
