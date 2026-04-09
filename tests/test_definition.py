import pytest
from kabinet.api.schema import list_definitions


@pytest.mark.integration
@pytest.mark.skip(
    reason="This test is meant to be run manually, as it requires a deployed app with the kabinet service"
)
def test_list_definition(deployed_app) -> None:
    x = list_definitions()
    assert len(x) > 0, "Was not able to find any definitions"
