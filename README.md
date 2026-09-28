# kabinet

[![codecov](https://codecov.io/gh/jhnnsrs/kabinet/branch/main/graph/badge.svg?token=UGXEA2THBV)](https://codecov.io/gh/jhnnsrs/kabinet)
[![PyPI version](https://badge.fury.io/py/kabinet.svg)](https://pypi.org/project/kabinet/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://pypi.org/project/kabinet/)
![Maintainer](https://img.shields.io/badge/maintainer-jhnnsrs-blue)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/kabinet.svg)](https://pypi.python.org/pypi/kabinet/)
[![PyPI download month](https://img.shields.io/pypi/dm/kabinet.svg)](https://pypi.python.org/pypi/kabinet/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/jhnnsrs/kabinet)

The python client for kabinet, the [Arkitekt](https://arkitekt.live) service that manages the
installable apps of a deployment: the repositories they come from, their releases and flavours, and
the deployments and pods that run them. It is the successor to the port spec.

## Installation

```bash
pip install kabinet
```

With arkitekt, `pip install "arkitekt[rekuest,kabinet]"` brings it in.

## Usage

Every kabinet operation is a method of the `Kabinet` client, in a blocking and an `a`-prefixed async
flavour (`kabinet.get_pod(id)`, `await kabinet.aget_pod(id)`). Nothing is looked up ambiently.

### In an arkitekt app

Add the service to your app and ask for `kabinet: Kabinet`; the client is injected by annotation.
Pods, deployments, releases, approvals, definitions and flavours travel between actions by id
(`@kabinet/pod`, `@kabinet/deployment`, `@kabinet/release`, `@kabinet/approval`,
`@kabinet/definition`, `@kabinet/flavour`), so an action can take and return them directly:

```python
from arkitekt import App, run
from kabinet import Kabinet, kabinet_service
from kabinet.api.schema import Pod

app = App("pod-status", "0.1.0", services=[kabinet_service])


@app.action
def pod_status(pod: Pod, kabinet: Kabinet) -> str:
    """Pod Status

    Fetches the current status of a pod.
    """
    return kabinet.get_pod(pod.id).status.value


if __name__ == "__main__":
    run(app)
```

### From a script

```python
from arkitekt import easy
from kabinet import kabinet_service

with easy("my-script", kabinet_service) as kabinet:
    repo = kabinet.create_github_repo(
        name="A new repo",
        identifier="jhnnsrs/kabinet:main",
    )
    print(repo)  # the repo with all the app images found in it
```

## Testing

```bash
uv run pytest -m "not integration"   # fast unit layer: no docker, <1s
uv run pytest                        # full suite: spins the dokker compose stack
```

The unit layer proves the wire contract through a rath `AsyncMockLink`
(camelCase aliases, `@oneOf` ordering variants, the six-kind selector union,
the `PodEvent` subscription shape) and the arkitekt service wiring via a
hot-plugged `fakts.testing.TestingFakts`. The `integration`-marked tests
run the same operations against the composed server image; until a
new-generation `jhnnsrs/kabinet:next` is pushed, point them at a locally
built image with `KABINET_SERVICE_IMAGE=next-kabinet:latest uv run pytest`.

See [RELEASING.md](RELEASING.md) for how versions are cut.
