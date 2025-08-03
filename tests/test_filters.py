import pytest
from kabinet.api.schema import list_flavours, FlavourFilter, FlavourOrder, Ordering


@pytest.mark.integration
def test_list_definition(deployed_app) -> None:
    z = list_flavours(
        filters=FlavourFilter(hasDefinitions=[15]),
        order=FlavourOrder(releasedAt=Ordering.DESC),
    )

    for flavour in z:
        print(flavour.name)