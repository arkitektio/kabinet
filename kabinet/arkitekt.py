"""The kabinet service of an arkitekt app, and the types it sends by id.

Declared on one registry: the service first, then the structures whose expanders
ask for the client it returns. An app takes all of it in with
``App(services=[kabinet_service])``.
"""

import os
from typing import Annotated

from fakts import Alias, Require, TokenLoader
from fakts.contrib.rath.auth import FaktsAuthLink
from graphql import OperationType
from rath.links.aiohttp import AIOHttpLink
from rath.links.graphql_ws import GraphQLWSLink
from rath.links.split import SplitLink

from rekuest.app import AppRegistry
from rekuest.widgets import SearchWidget

from kabinet.api.schema import (
    Definition,
    Deployment,
    Flavour,
    Pod,
    Release,
    SearchDefinitionsQuery,
    SearchDeploymentsQuery,
    SearchFlavoursQuery,
    SearchPodsQuery,
    SearchReleasesQuery,
)
from kabinet.kabinet import Kabinet
from kabinet.rath import KabinetLinkComposition, KabinetRath


def build_relative_path(*path: str) -> str:
    """Build a path relative to this file, for the files shipped beside it."""
    return os.path.join(os.path.dirname(__file__), *path)


registry = AppRegistry()
"""What kabinet brings to an app: its service, and the types it can send by id."""


@registry.service(
    schema=build_relative_path("api", "schema.graphql"),
    turms=build_relative_path("api", "project.json"),
)
def kabinet(
    kabinet: Annotated[
        Alias,
        Require("live.arkitekt.kabinet", "Where this deployment's apps and pods are managed"),
    ],
    tokens: TokenLoader,
) -> Kabinet:
    """Kabinet: the apps and pods a deployment runs."""
    return Kabinet(
        rath=KabinetRath(
            link=KabinetLinkComposition(
                auth=FaktsAuthLink(token_loader=tokens),
                split=SplitLink(
                    left=AIOHttpLink(endpoint_url=kabinet.to_http_path("graphql")),
                    right=GraphQLWSLink(ws_endpoint_url=kabinet.to_ws_path("graphql")),
                    split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                ),
            )
        )
    )


def _search(query: object) -> SearchWidget:
    """The widget that picks one of these out of the deployment."""
    return SearchWidget(query=query.Meta.document, ward="kabinet")  # type: ignore[attr-defined]


@registry.structure("@kabinet/pod", widget=_search(SearchPodsQuery))
async def expand_pod(id: str, kabinet: Kabinet) -> Pod:
    """A pod, by id."""
    return await kabinet.aget_pod(id)


@registry.structure("@kabinet/deployment", widget=_search(SearchDeploymentsQuery)
)
async def expand_deployment(id: str, kabinet: Kabinet) -> Deployment:
    """A deployment, by id."""
    return await kabinet.aget_deployment(id)


@registry.structure("@kabinet/release", widget=_search(SearchReleasesQuery))
async def expand_release(id: str, kabinet: Kabinet) -> Release:
    """A release, by id."""
    return await kabinet.aget_release(id)


@registry.structure("@kabinet/definition", widget=_search(SearchDefinitionsQuery)
)
async def expand_definition(id: str, kabinet: Kabinet) -> Definition:
    """A definition, by id."""
    return await kabinet.aget_definition(id)


@registry.structure("@kabinet/flavour", widget=_search(SearchFlavoursQuery))
async def expand_flavour(id: str, kabinet: Kabinet) -> Flavour:
    """A flavour, by id."""
    return await kabinet.aget_flavour(id)
