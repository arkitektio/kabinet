from kabinet.api.schema import CpuSelectorInput


def test_cpu_selector_input() -> None:
    """Test the CPU selector input."""
    selector = CpuSelectorInput(frequency=200, memory=2000)
    assert selector.frequency == 200
    assert selector.memory == 2000
