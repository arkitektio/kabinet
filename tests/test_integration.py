import pytest
from kabinet.api.schema import create_github_repo


@pytest.mark.integration
def test_create_cluster(deployed_app):
    x = create_github_repo(name="test", branch="main", user="jhnnsrs", repo="beta")
    assert x.id, "Was not able to create a cluster"
