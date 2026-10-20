"""kabinet's demands on its callers name structures kabinet really declares.

A demand that names an identifier nobody declares matches nothing, silently: the asking app
would never find the approval it needs.
"""

import pytest

pytest.importorskip("rekuest")

from arkitekt_spec.actions import PortKind  # noqa: E402

from kabinet import arkitekt as declared  # noqa: E402
from kabinet.callers import APPROVAL, RELEASE, REQUEST_APPROVAL  # noqa: E402


def test_request_approval_takes_a_release_and_a_deployer_and_returns_an_approval() -> None:
    """The demand an approving caller must meet: (release, deployer) -> approval."""
    registered = set(declared.registry.structure_registry.identifier_structure_map)
    assert {RELEASE, APPROVAL} <= registered

    release, agent = REQUEST_APPROVAL.arg_matches
    [ret] = REQUEST_APPROVAL.return_matches
    assert (release.at, release.kind, release.identifier) == (0, PortKind.STRUCTURE, RELEASE)
    assert (agent.at, agent.key, agent.kind) == (1, "agent", PortKind.STRING)
    assert (ret.kind, ret.identifier) == (PortKind.STRUCTURE, APPROVAL)
    assert (REQUEST_APPROVAL.force_arg_length, REQUEST_APPROVAL.force_return_length) == (2, 1)
