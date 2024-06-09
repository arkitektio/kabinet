from konviktion.funcs import execute, aexecute
from typing import Optional, List, Tuple, Literal
from enum import Enum
from pydantic import BaseModel, Field
from konviktion.rath import KonviktionRath


class UsersQueryUsers(BaseModel):
    typename: Optional[Literal["NotionUser"]] = Field(alias="__typename", exclude=True)
    id: str

    class Config:
        """A config class"""

        frozen = True


class UsersQuery(BaseModel):
    users: Tuple[UsersQueryUsers, ...]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "query Users {\n  users {\n    id\n  }\n}"


async def ausers(rath: Optional[KonviktionRath] = None) -> List[UsersQueryUsers]:
    """Users



    Arguments:
        rath (konviktion.rath.KonviktionRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        List[UsersQueryUsers]"""
    return (await aexecute(UsersQuery, {}, rath=rath)).users


def users(rath: Optional[KonviktionRath] = None) -> List[UsersQueryUsers]:
    """Users



    Arguments:
        rath (konviktion.rath.KonviktionRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        List[UsersQueryUsers]"""
    return execute(UsersQuery, {}, rath=rath).users
