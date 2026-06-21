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
    declare_backend,
    declare_resource,
    get_backend,
    list_backends,
    list_definitions,
    list_deployments,
    list_flavours,
    list_pod,
    list_releases,
    list_resources,
    search_backends,
)


@pytest.mark.integration
def test_create_repo(deployed_app) -> None:
    pass


@pytest.mark.integration
def test_declare_backend(deployed_app) -> None:
    """Declaring a backend returns a Backend with the given name."""
    rath = deployed_app.kabinet.rath

    backend = declare_backend(name="test-backend", kind="apptainer", rath=rath)

    assert isinstance(backend, Backend)
    assert backend.id
    assert backend.name == "test-backend"


@pytest.mark.integration
def test_declare_backend_is_idempotent(deployed_app) -> None:
    """Declaring the same backend twice returns the same backend."""
    rath = deployed_app.kabinet.rath

    first = declare_backend(name="idempotent-backend", kind="apptainer", rath=rath)
    second = declare_backend(name="idempotent-backend", kind="apptainer", rath=rath)

    assert first.id == second.id


@pytest.mark.integration
def test_list_backends(deployed_app) -> None:
    """A declared backend shows up in the list of backends."""
    rath = deployed_app.kabinet.rath

    backend = declare_backend(name="listed-backend", kind="apptainer", rath=rath)

    backends = list_backends(rath=rath)

    assert all(isinstance(b, ListBackend) for b in backends)
    assert backend.id in {b.id for b in backends}


@pytest.mark.integration
def test_get_backend(deployed_app) -> None:
    """A declared backend can be fetched by id."""
    rath = deployed_app.kabinet.rath

    backend = declare_backend(name="gettable-backend", kind="apptainer", rath=rath)

    fetched = get_backend(id=backend.id, rath=rath)

    assert fetched.id == backend.id
    assert fetched.name == backend.name


@pytest.mark.integration
def test_search_backends(deployed_app) -> None:
    """A declared backend is found through the search options query."""
    rath = deployed_app.kabinet.rath

    backend = declare_backend(name="searchable-backend", kind="apptainer", rath=rath)

    options = search_backends(search="searchable", rath=rath)

    assert backend.id in {o.value for o in options}


@pytest.mark.integration
def test_declare_resource(deployed_app) -> None:
    """A resource can be declared on a backend and references that backend."""
    rath = deployed_app.kabinet.rath

    backend = declare_backend(name="resource-backend", kind="apptainer", rath=rath)
    resource = declare_resource(
        backend=backend.id,
        local_id="resource-local-id",
        name="test-resource",
        rath=rath,
    )

    assert isinstance(resource, Resource)
    assert resource.id
    assert resource.name == "test-resource"
    assert resource.backend.id == backend.id


@pytest.mark.integration
def test_declare_resource_is_idempotent(deployed_app) -> None:
    """Declaring the same resource on a backend twice returns the same resource."""
    rath = deployed_app.kabinet.rath

    backend = declare_backend(name="resource-backend-2", kind="apptainer", rath=rath)
    first = declare_resource(
        backend=backend.id, local_id="same-local-id", rath=rath
    )
    second = declare_resource(
        backend=backend.id, local_id="same-local-id", rath=rath
    )

    assert first.id == second.id


@pytest.mark.integration
def test_list_resources(deployed_app) -> None:
    """A declared resource shows up in the list of resources."""
    rath = deployed_app.kabinet.rath

    backend = declare_backend(name="listed-resource-backend", kind="apptainer", rath=rath)
    resource = declare_resource(
        backend=backend.id, local_id="listed-resource", rath=rath
    )

    resources = list_resources(rath=rath)

    assert all(isinstance(r, ListResource) for r in resources)
    assert resource.id in {r.id for r in resources}


@pytest.mark.integration
def test_list_definitions(deployed_app) -> None:
    """Listing definitions returns a (possibly empty) tuple of ListDefinition."""
    rath = deployed_app.kabinet.rath

    definitions = list_definitions(rath=rath)

    assert isinstance(definitions, tuple)
    assert all(isinstance(d, ListDefinition) for d in definitions)


@pytest.mark.integration
def test_list_deployments(deployed_app) -> None:
    """Listing deployments returns a (possibly empty) tuple of ListDeployment."""
    rath = deployed_app.kabinet.rath

    deployments = list_deployments(rath=rath)

    assert isinstance(deployments, tuple)
    assert all(isinstance(d, ListDeployment) for d in deployments)


@pytest.mark.integration
def test_list_pods(deployed_app) -> None:
    """Listing pods returns a (possibly empty) tuple of ListPod."""
    rath = deployed_app.kabinet.rath

    pods = list_pod(rath=rath)

    assert isinstance(pods, tuple)
    assert all(isinstance(p, ListPod) for p in pods)


@pytest.mark.integration
def test_list_releases(deployed_app) -> None:
    """Listing releases returns a (possibly empty) tuple of ListRelease."""
    rath = deployed_app.kabinet.rath

    releases = list_releases(rath=rath)

    assert isinstance(releases, tuple)
    assert all(isinstance(r, ListRelease) for r in releases)


@pytest.mark.integration
def test_list_flavours(deployed_app) -> None:
    """Listing flavours returns a tuple without raising."""
    rath = deployed_app.kabinet.rath

    flavours = list_flavours(rath=rath)

    assert isinstance(flavours, tuple)
