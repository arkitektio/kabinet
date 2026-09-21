import pytest

from kabinet.api.schema import (
    Backend,
    ListBackend,
    ListDefinition,
    ListDeployment,
    ListPod,
    ListRelease,
    ListResource,
    Resource,
)
from kabinet.kabinet import Kabinet


@pytest.mark.integration
def test_create_repo(deployed_app) -> None:
    pass


@pytest.mark.integration
def test_declare_backend(kabinet: Kabinet) -> None:
    """Declaring a backend returns a Backend with the given name."""
    backend = kabinet.declare_backend(name="test-backend", kind="apptainer")

    assert isinstance(backend, Backend)
    assert backend.id
    assert backend.name == "test-backend"


@pytest.mark.integration
def test_declare_backend_is_idempotent(kabinet: Kabinet) -> None:
    """Declaring the same backend twice returns the same backend."""
    first = kabinet.declare_backend(name="idempotent-backend", kind="apptainer")
    second = kabinet.declare_backend(name="idempotent-backend", kind="apptainer")

    assert first.id == second.id


@pytest.mark.integration
def test_list_backends(kabinet: Kabinet) -> None:
    """A declared backend shows up in the list of backends."""
    backend = kabinet.declare_backend(name="listed-backend", kind="apptainer")

    backends = kabinet.list_backends()

    assert all(isinstance(b, ListBackend) for b in backends)
    assert backend.id in {b.id for b in backends}


@pytest.mark.integration
def test_get_backend(kabinet: Kabinet) -> None:
    """A declared backend can be fetched by id."""
    backend = kabinet.declare_backend(name="gettable-backend", kind="apptainer")

    fetched = kabinet.get_backend(id=backend.id)

    assert fetched.id == backend.id
    assert fetched.name == backend.name


@pytest.mark.integration
def test_search_backends(kabinet: Kabinet) -> None:
    """A declared backend is found through the search options query."""
    backend = kabinet.declare_backend(name="searchable-backend", kind="apptainer")

    options = kabinet.search_backends(search="searchable")

    assert backend.id in {o.value for o in options}


@pytest.mark.integration
def test_declare_resource(kabinet: Kabinet) -> None:
    """A resource can be declared on a backend and references that backend."""
    backend = kabinet.declare_backend(name="resource-backend", kind="apptainer")
    resource = kabinet.declare_resource(
        backend=backend.id,
        local_id="resource-local-id",
        name="test-resource",
    )

    assert isinstance(resource, Resource)
    assert resource.id
    assert resource.name == "test-resource"
    assert resource.backend.id == backend.id


@pytest.mark.integration
def test_declare_resource_is_idempotent(kabinet: Kabinet) -> None:
    """Declaring the same resource on a backend twice returns the same resource."""
    backend = kabinet.declare_backend(name="resource-backend-2", kind="apptainer")
    first = kabinet.declare_resource(
        backend=backend.id, local_id="same-local-id",
    )
    second = kabinet.declare_resource(
        backend=backend.id, local_id="same-local-id",
    )

    assert first.id == second.id


@pytest.mark.integration
def test_list_resources(kabinet: Kabinet) -> None:
    """A declared resource shows up in the list of resources."""
    backend = kabinet.declare_backend(name="listed-resource-backend", kind="apptainer")
    resource = kabinet.declare_resource(
        backend=backend.id, local_id="listed-resource",
    )

    resources = kabinet.list_resources()

    assert all(isinstance(r, ListResource) for r in resources)
    assert resource.id in {r.id for r in resources}


@pytest.mark.integration
def test_list_definitions(kabinet: Kabinet) -> None:
    """Listing definitions returns a (possibly empty) tuple of ListDefinition."""
    definitions = kabinet.list_definitions()

    assert isinstance(definitions, tuple)
    assert all(isinstance(d, ListDefinition) for d in definitions)


@pytest.mark.integration
def test_list_deployments(kabinet: Kabinet) -> None:
    """Listing deployments returns a (possibly empty) tuple of ListDeployment."""
    deployments = kabinet.list_deployments()

    assert isinstance(deployments, tuple)
    assert all(isinstance(d, ListDeployment) for d in deployments)


@pytest.mark.integration
def test_list_pods(kabinet: Kabinet) -> None:
    """Listing pods returns a (possibly empty) tuple of ListPod."""
    pods = kabinet.list_pod()

    assert isinstance(pods, tuple)
    assert all(isinstance(p, ListPod) for p in pods)


@pytest.mark.integration
def test_list_releases(kabinet: Kabinet) -> None:
    """Listing releases returns a (possibly empty) tuple of ListRelease."""
    releases = kabinet.list_releases()

    assert isinstance(releases, tuple)
    assert all(isinstance(r, ListRelease) for r in releases)


@pytest.mark.integration
def test_list_flavours(kabinet: Kabinet) -> None:
    """Listing flavours returns a tuple without raising."""
    flavours = kabinet.list_flavours()

    assert isinstance(flavours, tuple)
