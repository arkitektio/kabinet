"""A backend's pod lifecycle, called exactly as a deployer calls it.

The client sends only the arguments that were set, so this is also the contract
test for every nullable input the deployer leaves out: ``update_pod`` by local id
alone once failed on the server for want of ``pod``.

The server keys a backend to the calling client, so every test of a session shares
one: pods are checked by membership, never by the whole listing.
"""

import uuid

import pytest

from kabinet.api.schema import PodStatus, Release
from kabinet.kabinet import Kabinet

AGENT = "live.arkitekt.deployer"


@pytest.mark.integration
def test_a_backend_drives_its_pods_by_local_id(kabinet: Kabinet, release: Release) -> None:
    backend = kabinet.declare_backend(name=f"lifecycle-{uuid.uuid4().hex[:6]}", kind="docker")
    resource = kabinet.declare_resource(backend=backend.id, local_id="host:docker", name="host")
    approval = kabinet.approve_release(
        release.id, mandate="mandate-1", agent=AGENT, digest=release.approval_digest, backends=[backend.id]
    )
    deployment = kabinet.create_deployment(
        local_id=f"image-{uuid.uuid4().hex[:6]}", flavour=release.flavours[0].id, approval=approval.id
    )

    # The deployer names the pod before anything runs, and the pod starts PENDING.
    pod_key = uuid.uuid4().hex
    pod = kabinet.create_pod(deployment=deployment.id, local_id=pod_key, resource=resource.id)
    assert pod.pod_id == pod_key
    assert pod.status == PodStatus.PENDING

    # By local id alone: `pod` is left out of the input entirely.
    updated = kabinet.update_pod(local_id=pod_key, status=PodStatus.RUNNING)
    assert updated.id == pod.id
    assert updated.status == PodStatus.RUNNING

    # Creating again upserts: it only fills in the client the pod enrolled as.
    again = kabinet.create_pod(deployment=deployment.id, local_id=pod_key, resource=resource.id, client_id="client-1")
    assert again.id == pod.id
    assert again.client_id == "client-1"

    assert kabinet.my_pod_at(pod_key).id == pod.id
    assert pod.id in {p.id for p in kabinet.my_pods(backend.id, limit=1000)}

    kabinet.dump_logs(pod.id, "the reason it failed")
    kabinet.delete_pod(pod.id)

    # Gone is an answer, not an error: what decides that a container is an orphan.
    assert kabinet.my_pod_at(pod_key) is None
    assert pod.id not in {p.id for p in kabinet.my_pods(backend.id, limit=1000)}


@pytest.mark.integration
def test_my_pods_pages_in_a_stable_order(kabinet: Kabinet, release: Release) -> None:
    backend = kabinet.declare_backend(name=f"paging-{uuid.uuid4().hex[:6]}", kind="docker")
    approval = kabinet.approve_release(
        release.id, mandate="mandate-1", agent=AGENT, digest=release.approval_digest, backends=[backend.id]
    )
    deployment = kabinet.create_deployment(
        local_id=f"image-{uuid.uuid4().hex[:6]}", flavour=release.flavours[0].id, approval=approval.id
    )
    created = {kabinet.create_pod(deployment=deployment.id, local_id=uuid.uuid4().hex).id for _ in range(5)}

    everything = [p.id for p in kabinet.my_pods(backend.id, limit=1000)]
    paged: list[str] = []
    while page := kabinet.my_pods(backend.id, limit=2, offset=len(paged)):
        assert len(page) <= 2
        paged.extend(p.id for p in page)

    assert paged == everything
    assert created <= set(paged)
