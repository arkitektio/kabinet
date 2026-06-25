import pytest
from kabinet.api.schema import flavour_order, list_flavours, Ordering, flavour_filter


@pytest.mark.integration
def test_list_definition(deployed_app) -> None:
    z = list_flavours(
        filters=flavour_filter(has_definitions=("15",)),
        ordering=[flavour_order(released_at=Ordering.DESC)],
    )

    for flavour in z:
        print(flavour.name)
