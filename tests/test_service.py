"""Unit test for ``Kabinet.from_fakts``, the binder a run builds the client with.

Uses a hot-plugged ``fakts.testing.TestingFakts`` — a real Fakts, no
monkeypatching — to resolve what the binder asks for. Skipped when
``arkitekt`` is not installed (it is not one of kabinet's dev deps: it
depends on kabinet itself).
"""

import pytest

pytest.importorskip("arkitekt")
fakts = pytest.importorskip("fakts")
if not hasattr(fakts, "build_testing_fakts"):  # pragma: no cover
    pytest.skip("installed fakts predates TestingFakts", allow_module_level=True)

from arkitekt_spec.declare.client import client_of  # noqa: E402
from fakts.testing import build_testing_fakts  # noqa: E402

from kabinet.kabinet import Kabinet  # noqa: E402


def test_building_wires_fakts_into_the_links() -> None:
    with build_testing_fakts(aliases={"kabinet": "http://testserver"}) as fakts:
        kabinet = Kabinet.from_fakts(kabinet=fakts.get_alias("kabinet"), tokens=fakts)

    assert isinstance(kabinet, Kabinet)
    composition = kabinet.rath.link
    # Auth is narrowed to a token loader; Fakts satisfies it structurally.
    assert composition.auth.token_loader is fakts
    # The address was resolved once, when the client was built: the links hold a
    # URL, not a key to look up again later.
    assert composition.split.left.endpoint_url == "http://testserver/graphql"
    assert composition.split.right.ws_endpoint_url == "ws://testserver/graphql"


def test_requirements_declare_the_kabinet_service() -> None:
    declared = client_of(Kabinet)
    assert declared is not None
    (requirement,) = declared.get_requirements()
    assert requirement.key == "kabinet"
    assert requirement.service == "live.arkitekt.kabinet"
