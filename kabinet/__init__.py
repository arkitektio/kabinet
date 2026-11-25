"""The kabinet package to interact to the kabinet service."""

from .kabinet import Kabinet

__all__ = ["Kabinet"]

# Marks every type kabinet sends by id, so an app using `Kabinet` finds them.
from . import structures as _structures  # noqa: E402, F401
