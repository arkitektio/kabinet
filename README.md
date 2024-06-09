# Konviktion

[![codecov](https://codecov.io/gh/jhnnsrs/konviktion/branch/main/graph/badge.svg?token=UGXEA2THBV)](https://codecov.io/gh/jhnnsrs/konviktion)
[![PyPI version](https://badge.fury.io/py/konviktion.svg)](https://pypi.org/project/konviktion/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://pypi.org/project/konviktion/)
![Maintainer](https://img.shields.io/badge/maintainer-jhnnsrs-blue)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/konviktion.svg)](https://pypi.python.org/pypi/konviktion/)
[![PyPI status](https://img.shields.io/pypi/status/konviktion.svg)](https://pypi.python.org/pypi/konviktion/)
[![PyPI download month](https://img.shields.io/pypi/dm/konviktion.svg)](https://pypi.python.org/pypi/konviktion/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/jhnnsrs/konviktion)


## Description

Konviktion is a simple, lightweight, notion gateway. It is designed to be used within
the Arkitekt Framework to allow users to easily add pages to their notion workspace.

This is the client library for Konviktion, wich can be found [here](https://github.com/arkitektio/konviktion-server).
More information will be added soon.

### Requirements

Konviktion standalone requires that you have docker installed on your machine. If you do not have docker installed, you can find
instructions for installing it [here](https://docs.docker.com/get-docker/). 
Also we require you to have at least Python3.9.

```bash
pip install konviktion
```

### Usage

While you can use docker to spin up a konviktion-server yourself, you can also use the `deployed` context manager to spin up
a local konviktion-server.
    
```python
from konviktion import deployed 
from konviktion.api.schema import create_github_repository

with deployed():

    

    

```

In the above example, we use the `deployed` context manager to spin up a a local konviktion-server, and are creating
a repo on github. Repositories are online collections of various Apps (in various releases and flaovurs), that can be
used to deploy containers running these apps.

More info to come soon. Stay tuned.




