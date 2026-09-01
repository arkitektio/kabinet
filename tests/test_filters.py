import pytest
from kabinet.api.schema import Ordering, flavour_filter, flavour_order, list_flavours

from .conftest import DeployedKabinet


@pytest.mark.integration
def test_flavour_filters_and_ordering(deployed_app: DeployedKabinet) -> None:
    """Filters and @oneOf ordering are accepted together by a real server."""
    flavours = list_flavours(
        filters=flavour_filter(search="definitely-not-a-real-flavour"),
        ordering=[flavour_order(released_at=Ordering.DESC)],
        rath=deployed_app.kabinet.rath,
    )
    assert flavours == ()

    unfiltered = list_flavours(
        ordering=[flavour_order(released_at=Ordering.DESC)],
        rath=deployed_app.kabinet.rath,
    )
    assert isinstance(unfiltered, tuple)
