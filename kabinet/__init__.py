"""The kabinet package to interact to the kabinet service."""

from .kabinet import Kabinet

# The service is declared with arkitekt-spec, a core dependency: it is always there.
from .arkitekt import kabinet as kabinet_service

__all__ = ["Kabinet", "kabinet_service"]
