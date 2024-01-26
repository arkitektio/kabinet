""" A deployed kluster instance package"""

from dokker import mirror, Deployment
import os
from koil.composition import Composition
from rath.links.auth import ComposedAuthLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.graphql_ws import GraphQLWSLink
from kabinet.rath import (
    KabinetRath,
    SplitLink,
    KabinetRathLinkComposition,
)
from kabinet.kabinet import Kabinet
from graphql import OperationType

test_path = os.path.join(os.path.dirname(__file__), "deployments", "test")


def build_deployment() -> Deployment:
    """Builds a deploymen of kluster for testing

    This will return a deployment of kluster that is ready to be used for testing.
    It will have a health check that will check the graphql endpoint.

    Returns
    -------
    Deployment
        The deployment of kluster (dokker.Deployment)


    """
    setup = mirror(test_path)
    setup.add_health_check(
        url="http://localhost:7766/graphql",
        service="kluster",
        timeout=5,
        max_retries=10,
    )
    return setup


async def token_loader() -> str:
    """Returns a token as defined in the static_token setting for kluster"""
    return "demo"


def build_deployed_kabinet() -> Kabinet:
    """Build a client for a  deployed kluster instance

    This will return a client for a deployed kluster instance. It will use the
    static_token setting for authentication.

    """

    y = KabinetRath(
        link=KabinetRathLinkComposition(
            auth=ComposedAuthLink(
                token_loader=token_loader,
                token_refresher=token_loader,
            ),
            split=SplitLink(
                left=AIOHttpLink(endpoint_url="http://localhost:7766/graphql"),
                right=GraphQLWSLink(ws_endpoint_url="ws://localhost:7766/graphql"),
                split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
            ),
        ),
    )

    omero_ark = Kabinet(rath=y)
    return omero_ark


class DeployedKabinet(Composition):
    """A deployed kluster instance

    THis is a composition of both a deployment of kluster-server
    (and kluster-gateway) and a client for that deployment. It is
    the fastest way to get a fully functioning kluster instance,
    ready for testing.


    """

    deployment: Deployment
    Kabinet: Kabinet




def static(url: str, token: str) -> Kabinet:

    async def token_loader() -> str:
        nonlocal token
        """Returns a token as defined in the static_token setting for kluster"""
        return token

    y = KabinetRath(
        link=KabinetRathLinkComposition(
            auth=ComposedAuthLink(
                token_loader=token_loader,
                token_refresher=token_loader,
            ),
            split=SplitLink(
                left=AIOHttpLink(endpoint_url=f"http://{url}/graphql"),
                right=GraphQLWSLink(ws_endpoint_url=f"ws://{url}/graphql"),
                split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
            ),
        ),
    )

    omero_ark = Kabinet(rath=y)
    return omero_ark







def deployed() -> DeployedKabinet:
    """Create a deployed kluster

    A deployed kluster is a composition of a deployment of the
    kluster server and a kluster client.
    This means a fully functioning kluster instance will be spun up when
    the context manager is entered.

    To inspect the deployment, use the `deployment` attribute.
    To interact with the kluster, use the `kluster` attribute.


    Returns
    -------
    DeployedKluster
        The deployed kluster instance (Composition)
    """
    return DeployedKabinet(
        deployment=build_deployment(),
        Kabinet=build_deployed_kabinet(),
    )
