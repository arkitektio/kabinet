"""The types kabinet sends by id: each expanded by the ``Kabinet`` client.

Imported by ``kabinet/__init__``, so each class is marked whenever kabinet is.
"""

from arkitekt_spec.declare.structures.declare import structure
from arkitekt_spec.declare.widgets import SearchWidget

from kabinet.api.schema import (
    Definition,
    Deployment,
    Flavour,
    Pod,
    Release,
    ReleaseApproval,
    SearchDefinitionsQuery,
    SearchDeploymentsQuery,
    SearchFlavoursQuery,
    SearchPodsQuery,
    SearchReleaseApprovalsQuery,
    SearchReleasesQuery,
)
from kabinet.kabinet import Kabinet


def _search(query: object) -> SearchWidget:
    """The widget that picks one of these out of the deployment."""
    return SearchWidget(query=query.Meta.document, ward="kabinet")  # type: ignore[attr-defined]


@structure("@kabinet/pod", widget=_search(SearchPodsQuery))
async def expand_pod(id: str, kabinet: Kabinet) -> Pod:
    """A pod, by id."""
    return await kabinet.aget_pod(id)


@structure("@kabinet/deployment", widget=_search(SearchDeploymentsQuery))
async def expand_deployment(id: str, kabinet: Kabinet) -> Deployment:
    """A deployment, by id."""
    return await kabinet.aget_deployment(id)


@structure("@kabinet/release", widget=_search(SearchReleasesQuery))
async def expand_release(id: str, kabinet: Kabinet) -> Release:
    """A release, by id."""
    return await kabinet.aget_release(id)


@structure("@kabinet/approval", widget=_search(SearchReleaseApprovalsQuery))
async def expand_release_approval(id: str, kabinet: Kabinet) -> ReleaseApproval:
    """A user's standing approval to run a release, by id."""
    return await kabinet.aget_release_approval(id)


@structure("@kabinet/definition", widget=_search(SearchDefinitionsQuery))
async def expand_definition(id: str, kabinet: Kabinet) -> Definition:
    """A definition, by id."""
    return await kabinet.aget_definition(id)


@structure("@kabinet/flavour", widget=_search(SearchFlavoursQuery))
async def expand_flavour(id: str, kabinet: Kabinet) -> Flavour:
    """A flavour, by id."""
    return await kabinet.aget_flavour(id)
