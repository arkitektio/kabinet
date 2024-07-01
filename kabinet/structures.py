"""Strucutre Registration"""

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
    structure_reg = None
