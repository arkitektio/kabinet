"""``SelectorInput`` is a discriminated union of per-kind input models
(``@unionElementOf`` in the server schema); the ``selector_input`` factory
dispatches to the right member by ``kind``. Every member carries the shared
``required``/``weight`` hard/soft split."""

import pytest
from pydantic import ValidationError

from kabinet.api.schema import (
    CpuSelectorInput,
    CudaSelectorInput,
    LabelSelectorInput,
    RamSelectorInput,
    selector_input,
)


def test_cpu_selector_variant_constructs_directly() -> None:
    selector = CpuSelectorInput(min_count=4, frequency=2400.0, arch="arm64")
    assert selector.kind == "cpu"
    assert selector.min_count == 4
    assert selector.arch == "arm64"


def test_cuda_selector_carries_the_nvidia_placement_fields() -> None:
    selector = CudaSelectorInput(compute_capability="8.6", memory=8000, count=2)
    assert selector.kind == "cuda"
    assert selector.compute_capability == "8.6"
    assert selector.memory == 8000
    assert selector.count == 2


def test_selector_input_factory_dispatches_by_kind() -> None:
    ram = selector_input(kind="ram", min=16000)
    assert isinstance(ram, RamSelectorInput)
    assert ram.min == 16000
    label = selector_input(kind="label", key="microscope", required=False, weight=10)
    assert isinstance(label, LabelSelectorInput)
    assert label.required is False and label.weight == 10


def test_selector_input_rejects_fields_of_the_wrong_kind() -> None:
    with pytest.raises(ValidationError):
        selector_input(kind="cpu", cuda_cores=99)


def test_cpu_memory_moved_to_the_ram_selector() -> None:
    """cpu.memory was removed from the vocabulary — system memory is ram's job."""
    with pytest.raises(ValidationError):
        CpuSelectorInput(memory=2000)
