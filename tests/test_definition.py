import pytest

from kabinet.kabinet import Kabinet


@pytest.mark.integration
@pytest.mark.skip(
    reason="This test is meant to be run manually, as it requires a deployed app with the kabinet service"
)
def test_list_definition(kabinet: Kabinet) -> None:
    x = kabinet.list_definitions()
    assert len(x) > 0, "Was not able to find any definitions"
