import pytest
from kabinet.api.schema import list_definitions


@pytest.mark.integration
def test_list_definition(deployed_app) -> None:
    x = list_definitions()
    assert len(x) > 0, "Was not able to find any definitions"
