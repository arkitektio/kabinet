"""The graphql rath client for  kabinet"""

from types import TracebackType
from pydantic import Field
from rath import rath

from rath.links.auth import AuthTokenLink

from rath.links.compose import TypedComposedLink
from rath.links.dictinglink import DictingLink
from rath.links.shrink import ShrinkingLink
from rath.links.split import SplitLink


class KabinetLinkComposition(TypedComposedLink):
    """Kabinet Link Composition"""

    shrinking: ShrinkingLink = Field(default_factory=ShrinkingLink)
    dicting: DictingLink = Field(default_factory=DictingLink)
    auth: AuthTokenLink
    split: SplitLink


class KabinetRath(rath.Rath):
    """Kabinet Rath

    Args:
        rath (_type_): _description_
    """

    async def __aenter__(self) -> "KabinetRath":
        """Enter the client.

        Entering does not make it "the current client": nothing is. Calls go
        through the ``Kabinet`` client they are made on.
        """
        await super().__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the client"""
        await super().__aexit__(exc_type, exc_val, exc_tb)
