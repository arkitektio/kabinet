"""Release approvals, end to end against a real kabinet.

A user approves a release for a deployer, pinned to the release's digest; only
under an active approval that allows the calling backend may a flavour of that
release be deployed. The release is registered with ``create_app_image``, as a
build pushes it, so nothing depends on scanning a repository.
"""

import uuid
from datetime import datetime

import pytest
from rath.operation import GraphQLException

from kabinet.api.schema import (
    DockerImageInput,
    InspectionInput,
    ManifestInput,
    Release,
    ReleaseApproval,
)
from kabinet.kabinet import Kabinet

AGENT = "live.arkitekt.deployer"


@pytest.fixture
def release(kabinet: Kabinet) -> Release:
    """A fresh release with one flavour, unique to the test."""
    identifier = f"com.example.approved-{uuid.uuid4().hex[:8]}"
    return kabinet.create_app_image(
        manifest=ManifestInput(identifier=identifier, version="1.0.0", scopes=["read"]),
        selectors=[],
        app_image_id=uuid.uuid4().hex,
        inspection=InspectionInput(
            size=1,
            locks=[],
            implementations=[],
            states=[],
            requirements=[],
        ),
        image=DockerImageInput(image_string=f"example/{identifier}:1.0.0", build_at=datetime.now()),
        flavour_name="vanilla",
    )


def _approve(kabinet: Kabinet, release: Release, **extra) -> ReleaseApproval:
    return kabinet.approve_release(
        release.id, mandate="mandate-1", agent=AGENT, digest=release.approval_digest, **extra
    )


@pytest.mark.integration
def test_a_release_carries_what_an_approval_pins(release: Release) -> None:
    assert release.approval_digest
    assert release.mandate_manifest["identifier"] == release.app.identifier
    assert len(release.flavours) == 1


@pytest.mark.integration
def test_an_approval_is_active_and_found(kabinet: Kabinet, release: Release) -> None:
    approval = _approve(kabinet, release)

    assert approval.is_active and not approval.is_stale
    assert approval.revoked_at is None
    assert approval.agent == AGENT
    assert approval.digest == release.approval_digest
    assert approval.release.id == release.id

    assert kabinet.get_release_approval(approval.id).id == approval.id
    assert approval.id in [a.id for a in kabinet.list_release_approvals()]
    assert approval.id in [o.value for o in kabinet.search_release_approvals()]


@pytest.mark.integration
def test_an_approval_of_a_changed_release_is_refused(kabinet: Kabinet, release: Release) -> None:
    with pytest.raises(GraphQLException, match="changed since you reviewed"):
        kabinet.approve_release(release.id, mandate="mandate-1", agent=AGENT, digest="not-the-digest")


@pytest.mark.integration
def test_deploying_needs_an_active_approval_for_this_backend(kabinet: Kabinet, release: Release) -> None:
    backend = kabinet.declare_backend(name="approvals-backend", kind="apptainer")
    flavour = release.flavours[0]
    approval = _approve(kabinet, release, backends=[backend.id])

    deployment = kabinet.create_deployment(
        local_id=f"local-{uuid.uuid4().hex[:8]}", flavour=flavour.id, approval=approval.id
    )
    assert deployment.id

    revoked = kabinet.revoke_approval(approval.id)
    assert revoked.revoked_at is not None
    assert not revoked.is_active

    with pytest.raises(GraphQLException):
        kabinet.create_deployment(
            local_id=f"local-{uuid.uuid4().hex[:8]}", flavour=flavour.id, approval=approval.id
        )
