"""Wire-serialization unit tests for the generated kabinet client.

No docker, no network: an ``AsyncMockLink`` terminates the rath chain, so
these prove what goes onto the wire (camelCase aliases, ``@oneOf`` ordering
variants) and that responses parse back into the typed models — including the
selector union with all six implementors and the new ``PodEvent``
subscription shape. The dokker integration suite covers the same operations
against a real server.
"""

from typing import Any, AsyncIterator

from rath.links.testing.mock import AsyncMockLink
from rath.operation import Operation

from kabinet.api.schema import (
    ListFlavourSelectorsBaseCatchAll,
    ListFlavourSelectorsBaseCPUSelector,
    ListFlavourSelectorsBaseCudaSelector,
    ListFlavourSelectorsBaseLabelSelector,
    ListFlavourSelectorsBaseOneApiSelector,
    ListFlavourSelectorsBaseRAMSelector,
    Ordering,
    flavour_order,
)
from kabinet.kabinet import Kabinet
from kabinet.rath import KabinetRath


def client(link: AsyncMockLink) -> Kabinet:
    """A client whose rath ends in ``link``: calls are its methods."""
    return Kabinet(rath=KabinetRath(link=link))


def flavour_payload(selectors: list | None = None, **overrides: Any) -> dict:
    """A minimal valid payload for the ``ListFlavour`` fragment."""
    payload = {
        "id": "1",
        "name": "vanilla",
        "image": {"imageString": "org/app:latest", "buildAt": "2026-01-01T00:00:00Z"},
        "manifest": {},
        "requirements": [],
        "repo": None,
        "selectors": selectors or [],
    }
    payload.update(overrides)
    return payload


def full_flavour_payload() -> dict:
    """The ``Flavour`` fragment: ListFlavour plus its release."""
    return flavour_payload() | {
        "release": {
            "id": "1",
            "version": "0.0.1",
            "app": {"identifier": "org/app"},
            "scopes": [],
        }
    }


def pod_payload(id: str = "1") -> dict:
    return {
        "id": id,
        "podId": f"pod-{id}",
        "deployment": {"flavour": full_flavour_payload()},
    }


async def test_declare_backend_serializes_input() -> None:
    captured: dict = {}

    async def resolve(operation: Operation) -> dict:
        captured.update(operation.variables)
        return {"id": "1", "name": "my-backend"}

    async with client(AsyncMockLink(mutation_resolver={"declareBackend": resolve})) as kabinet:
        backend = await kabinet.adeclare_backend(name="my-backend", kind="docker")

    assert captured["input"] == {"name": "my-backend", "kind": "docker"}
    assert backend.name == "my-backend"


async def test_oneof_flavour_ordering_serializes_single_key() -> None:
    """The ``@oneOf`` order input must hit the wire as exactly one aliased key."""
    captured: dict = {}

    async def resolve(operation: Operation) -> list:
        captured.update(operation.variables)
        return []

    async with client(AsyncMockLink(query_resolver={"flavours": resolve})) as kabinet:
        await kabinet.alist_flavours(ordering=[flavour_order(released_at=Ordering.DESC)])

    assert captured["ordering"] == [{"releasedAt": "DESC"}]


async def test_selector_union_parses_all_kinds() -> None:
    """Every selector implementor — including kinds the fragment does not
    know — parses into its variant class (unknown kinds land in CatchAll),
    and the interface's ``weight`` is available on all of them."""
    selectors = [
        {"__typename": "CudaSelector", "kind": "cuda", "required": True, "weight": 2,
         "computeCapability": "8.6", "cudaVersion": "12", "memory": 8000, "count": 2,
         "cudaCores": 100},
        {"__typename": "CPUSelector", "kind": "cpu", "required": True, "weight": 1,
         "minCount": 4, "frequency": 2400.0, "arch": "arm64"},
        {"__typename": "RAMSelector", "kind": "ram", "required": True, "weight": 1,
         "min": 1024},
        {"__typename": "LabelSelector", "kind": "label", "required": False, "weight": 10,
         "key": "gpu", "value": "true"},
        {"__typename": "OneApiSelector", "kind": "oneapi", "required": True, "weight": 1,
         "oneapiVersion": "2024.1"},
        {"__typename": "SomeFutureSelector", "kind": "future", "required": False, "weight": 0},
    ]

    async def resolve(operation: Operation) -> list:
        return [flavour_payload(selectors=selectors)]

    async with client(AsyncMockLink(query_resolver={"flavours": resolve})) as kabinet:
        flavours = await kabinet.alist_flavours()

    parsed = flavours[0].selectors
    assert isinstance(parsed[0], ListFlavourSelectorsBaseCudaSelector)
    assert parsed[0].compute_capability == "8.6"
    assert parsed[0].memory == 8000
    assert parsed[0].count == 2
    assert isinstance(parsed[1], ListFlavourSelectorsBaseCPUSelector)
    assert parsed[1].min_count == 4
    assert parsed[1].arch == "arm64"
    assert isinstance(parsed[2], ListFlavourSelectorsBaseRAMSelector)
    assert parsed[2].min == 1024
    assert isinstance(parsed[3], ListFlavourSelectorsBaseLabelSelector)
    assert parsed[3].key == "gpu"
    assert isinstance(parsed[4], ListFlavourSelectorsBaseOneApiSelector)
    assert parsed[4].oneapi_version == "2024.1"
    # Unknown future kinds must not break parsing — they land in the
    # catch-all with the shared interface fields.
    assert isinstance(parsed[5], ListFlavourSelectorsBaseCatchAll)
    assert all(s.weight >= 0 for s in parsed)


async def test_watch_pods_yields_pod_events() -> None:
    """The new ``PodEvent`` subscription shape: create/update carry a Pod,
    delete carries the ID."""

    async def events(operation: Operation) -> AsyncIterator[dict]:
        yield {"create": pod_payload("1"), "update": None, "delete": None}
        yield {"create": None, "update": None, "delete": "1"}

    async with client(AsyncMockLink(subscription_resolver={"pods": events})) as kabinet:
        seen = [event async for event in kabinet.awatch_pods()]

    assert seen[0].create is not None and seen[0].create.pod_id == "pod-1"
    assert seen[0].delete is None
    assert seen[1].delete == "1"
