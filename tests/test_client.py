"""A kabinet call goes through the client it is made on, and nothing else.

No server: the rath is a fake returning canned data.
"""

from types import SimpleNamespace
from typing import Any, AsyncIterator, Optional

import pytest
from pydantic import BaseModel, ConfigDict
from rath.links.testing.mock import AsyncMockLink
from rath.operation import Operation
from rath.origin import ContextBound, get_origin

from kabinet.api.schema import KabinetApi
from kabinet.kabinet import Kabinet
from kabinet.rath import KabinetRath


class FakeRath:
    """Answers every query with the same canned pod, and remembers what was sent."""

    def __init__(self) -> None:
        self.sent: list[dict[str, Any]] = []

    def _answer(self, variables: dict[str, Any]) -> Any:
        self.sent.append(variables)
        return SimpleNamespace(data={"pod": {"id": "pod-1", "backend": {"id": "b-1"}}})

    async def aquery(self, document: str, variables: dict[str, Any]) -> Any:
        return self._answer(variables)

    async def asubscribe(self, document: str, variables: dict[str, Any]) -> AsyncIterator[Any]:
        yield self._answer(variables)


class Backend(ContextBound):
    model_config = ConfigDict(frozen=True)
    id: str


class Pod(ContextBound):
    model_config = ConfigDict(frozen=True)
    id: str
    backend: Backend


class GetPod(BaseModel):
    """Shaped like a generated operation."""

    pod: Pod

    class Arguments(BaseModel):
        id: str
        note: Optional[str] = None

    class Meta:
        document = "query GetPod($id: ID!) { pod(id: $id) { id backend { id } } }"


def client() -> Kabinet:
    """The real client over a fake rath (built without validating the field)."""
    return Kabinet.model_construct(rath=FakeRath())


@pytest.mark.asyncio
async def test_aexecute_goes_through_the_client_and_results_remember_it() -> None:
    mine, other = client(), client()

    result = await mine.aexecute(GetPod, {"id": "pod-1"})

    assert (len(mine.rath.sent), len(other.rath.sent)) == (1, 0)
    origin = get_origin(result.pod.backend)
    assert origin is not None and origin.client is mine and origin.rath is mine.rath


def test_execute_goes_through_the_client() -> None:
    from koil import Koil

    mine = client()
    with Koil():
        assert mine.execute(GetPod, {"id": "pod-1"}).pod.id == "pod-1"
    assert len(mine.rath.sent) == 1


@pytest.mark.asyncio
async def test_asubscribe_goes_through_the_client() -> None:
    mine = client()
    events = [e async for e in mine.asubscribe(GetPod, {"id": "pod-1"})]
    assert [e.pod.id for e in events] == ["pod-1"]
    assert get_origin(events[0].pod).client is mine


def test_subscribe_goes_through_the_client() -> None:
    from koil import Koil

    mine = client()
    with Koil():
        events = list(mine.subscribe(GetPod, {"id": "pod-1"}))
    assert [e.pod.id for e in events] == ["pod-1"]
    assert get_origin(events[0].pod).client is mine


@pytest.mark.asyncio
async def test_unset_arguments_are_not_sent() -> None:
    """kabinet's wire behaviour, kept through the rewrite: exclude_unset."""
    mine = client()
    await mine.aexecute(GetPod, {"id": "pod-1"})
    assert mine.rath.sent == [{"id": "pod-1"}]


def test_every_operation_is_a_method_of_the_client() -> None:
    assert issubclass(Kabinet, KabinetApi)
    assert set(Kabinet.model_fields) == {"rath"}
    for name in ("aget_pod", "get_pod", "awatch_pods", "watch_pods", "adeclare_backend"):
        assert getattr(Kabinet, name) is getattr(KabinetApi, name)


def test_the_generated_module_has_no_module_level_operations() -> None:
    import kabinet.api.schema as schema

    assert not hasattr(schema, "aget_pod")
    assert not hasattr(schema, "declare_backend")


@pytest.mark.asyncio
async def test_generated_methods_go_through_their_own_client() -> None:
    """Two clients, one call each: every answer comes from the client it was made on."""
    asked: list[str] = []

    def backend_link(name: str) -> AsyncMockLink:
        async def resolve(operation: Operation) -> dict[str, Any]:
            asked.append(name)
            return {"id": "1", "name": name}

        return AsyncMockLink(mutation_resolver={"declareBackend": resolve})

    a, b = (Kabinet(rath=KabinetRath(link=backend_link(n))) for n in "ab")

    async with a, b:
        backend = await b.adeclare_backend(name="mine", kind="docker")

    assert asked == ["b"]
    assert backend.name == "b"


@pytest.mark.asyncio
async def test_generated_subscription_goes_through_its_client() -> None:
    async def events(operation: Operation) -> AsyncIterator[dict]:
        yield {"create": None, "update": None, "delete": "1"}

    kabinet = Kabinet(rath=KabinetRath(link=AsyncMockLink(subscription_resolver={"pods": events})))

    async with kabinet:
        seen = [event async for event in kabinet.awatch_pods()]

    assert [e.delete for e in seen] == ["1"]
