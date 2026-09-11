"""Unit test for the arkitekt service integration (``kabinet.arkitekt``).

Uses a hot-plugged ``fakts.testing.TestingFakts`` — a real Fakts, no
monkeypatching — to build the service the way ``easy()`` would. Skipped when
``arkitekt`` is not installed (it is not one of kabinet's dev deps: it
depends on kabinet itself).
"""

import pytest

pytest.importorskip("arkitekt")
fakts = pytest.importorskip("fakts")
if not hasattr(fakts, "build_testing_fakts"):  # pragma: no cover
    pytest.skip("installed fakts predates TestingFakts", allow_module_level=True)

from fakts.testing import build_testing_fakts  # noqa: E402

from kabinet.arkitekt import KabinetService  # noqa: E402
from kabinet.kabinet import Kabinet  # noqa: E402


def test_build_service_wires_fakts_into_the_links() -> None:
    with build_testing_fakts(aliases={"kabinet": "http://testserver"}) as fakts:
        service = KabinetService()
        kabinet = service.build_service(fakts, {})

    assert isinstance(kabinet, Kabinet)
    composition = kabinet.rath.link
    assert composition.auth.fakts is fakts
    assert composition.split.left.fakts_group == "kabinet"
    assert composition.split.right.fakts_group == "kabinet"


def test_requirements_declare_the_kabinet_service() -> None:
    (requirement,) = KabinetService().get_requirements()
    assert requirement.key == "kabinet"
    assert requirement.service == "live.arkitekt.kabinet"
