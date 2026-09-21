import pytest

from kabinet.api.schema import Ordering, flavour_filter, flavour_order
from kabinet.kabinet import Kabinet


@pytest.mark.integration
def test_flavour_filters_and_ordering(kabinet: Kabinet) -> None:
    """Filters and @oneOf ordering are accepted together by a real server."""
    flavours = kabinet.list_flavours(
        filters=flavour_filter(search="definitely-not-a-real-flavour"),
        ordering=[flavour_order(released_at=Ordering.DESC)],
    )
    assert flavours == ()

    unfiltered = kabinet.list_flavours(
        ordering=[flavour_order(released_at=Ordering.DESC)],
    )
    assert isinstance(unfiltered, tuple)
