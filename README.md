# Kabinet

[![codecov](https://codecov.io/gh/jhnnsrs/kabinet/branch/main/graph/badge.svg?token=UGXEA2THBV)](https://codecov.io/gh/jhnnsrs/kabinet)
[![PyPI version](https://badge.fury.io/py/kabinet.svg)](https://pypi.org/project/kabinet/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://pypi.org/project/kabinet/)
![Maintainer](https://img.shields.io/badge/maintainer-jhnnsrs-blue)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/kabinet.svg)](https://pypi.python.org/pypi/kabinet/)
[![PyPI status](https://img.shields.io/pypi/status/kabinet.svg)](https://pypi.python.org/pypi/kabinet/)
[![PyPI download month](https://img.shields.io/pypi/dm/kabinet.svg)](https://pypi.python.org/pypi/kabinet/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/jhnnsrs/kabinet)


## Description

Kabinet is a simple, lightweight, and easy to use container orchestration tool. It is designed to be used within
the Arkitekt Framework to visualize Containers that might be running on multiple machines, and on varying backends.
It also provides a simple interface to get the right container for the right job.

Kabinet is designed to be used with the Arkitekt Framework.

This is the client library for Kabinet, wich can be found [here](https://github.com/arkitektio/kabinet-server).
More information will be added soon.

### Requirements

Kabinet standalone requires that you have docker installed on your machine. If you do not have docker installed, you can find
instructions for installing it [here](https://docs.docker.com/get-docker/). 
Also we require you to have at least Python3.9.

```bash
pip install kabinet
```

### Usage

While you can use docker to spin up a kluster-server yourself, you can also use the `deployed` context manager to spin up
a local kluster-server.
    
```python
from kabinet import deployed 
from kabinet.api.schema import create_github_repository

with deployed():

    repo = create_github_repository(name="my-repo", user="jhnnsrs", repo="beta", branch="main")

    

```

In the above example, we use the `deployed` context manager to spin up a a local kabinet-server, and are creating
a repo on github. Repositories are online collections of various Apps (in various releases and flaovurs), that can be
used to deploy containers running these apps.

More info to come soon. Stay tuned.




