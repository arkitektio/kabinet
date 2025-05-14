from kabinet.api.schema import SelectorInput


def test_cpu_selector_input() -> None:
    """Test the CPU selector input."""
    selector = SelectorInput(frequency=200, memory=2000, kind="cpu")
    assert selector.frequency == 200
    assert selector.memory == 2000
