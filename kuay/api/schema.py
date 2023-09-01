from typing import Literal, Tuple, List, Optional
from pydantic import BaseModel, Field
from rath.scalars import ID
from enum import Enum
from kuay.rath import KuayRath
from kuay.funcs import aexecute, execute


class PullProgressStatus(str, Enum):
    """Docker pull progress status."""

    PULLING = "PULLING"
    PULLED = "PULLED"


class ContainerStatus(str, Enum):
    CREATED = "CREATED"
    RESTARTING = "RESTARTING"
    RUNNING = "RUNNING"
    REMOVING = "REMOVING"
    PAUSED = "PAUSED"
    EXITED = "EXITED"
    DEAD = "DEAD"


class DockerRuntime(str, Enum):
    """Docker runtime."""

    NVIDIA = "NVIDIA"
    RUNC = "RUNC"


class GithubRepoFragment(BaseModel):
    typename: Optional[Literal["GithubRepo"]] = Field(alias="__typename", exclude=True)
    user: str
    branch: str
    repo: str
    id: ID

    class Config:
        frozen = True


class Create_githubrepoMutation(BaseModel):
    create_github_repo: Optional[GithubRepoFragment] = Field(alias="createGithubRepo")

    class Arguments(BaseModel):
        branch: str
        user: str
        repo: str

    class Meta:
        document = "fragment GithubRepo on GithubRepo {\n  user\n  branch\n  repo\n  id\n}\n\nmutation create_githubrepo($branch: String!, $user: String!, $repo: String!) {\n  createGithubRepo(branch: $branch, user: $user, repo: $repo) {\n    ...GithubRepo\n  }\n}"


class Get_github_repoQuery(BaseModel):
    github_repo: Optional[GithubRepoFragment] = Field(alias="githubRepo")
    "Get information on your Docker Template"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment GithubRepo on GithubRepo {\n  user\n  branch\n  repo\n  id\n}\n\nquery get_github_repo($id: ID!) {\n  githubRepo(id: $id) {\n    ...GithubRepo\n  }\n}"


class Search_githubrepoQueryGithubrepos(BaseModel):
    typename: Optional[Literal["GithubRepo"]] = Field(alias="__typename", exclude=True)
    value: ID
    label: str

    class Config:
        frozen = True


class Search_githubrepoQuery(BaseModel):
    github_repos: Optional[
        Tuple[Optional[Search_githubrepoQueryGithubrepos], ...]
    ] = Field(alias="githubRepos")

    class Arguments(BaseModel):
        search: str

    class Meta:
        document = "query search_githubrepo($search: String!) {\n  githubRepos(name: $search) {\n    value: id\n    label: repo\n  }\n}"


async def acreate_githubrepo(
    branch: str, user: str, repo: str, rath: KuayRath = None
) -> Optional[GithubRepoFragment]:
    """create_githubrepo



    Arguments:
        branch (str): branch
        user (str): user
        repo (str): repo
        rath (kuay.rath.KuayRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[GithubRepoFragment]"""
    return (
        await aexecute(
            Create_githubrepoMutation,
            {"branch": branch, "user": user, "repo": repo},
            rath=rath,
        )
    ).create_github_repo


def create_githubrepo(
    branch: str, user: str, repo: str, rath: KuayRath = None
) -> Optional[GithubRepoFragment]:
    """create_githubrepo



    Arguments:
        branch (str): branch
        user (str): user
        repo (str): repo
        rath (kuay.rath.KuayRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[GithubRepoFragment]"""
    return execute(
        Create_githubrepoMutation,
        {"branch": branch, "user": user, "repo": repo},
        rath=rath,
    ).create_github_repo


async def aget_github_repo(
    id: ID, rath: KuayRath = None
) -> Optional[GithubRepoFragment]:
    """get_github_repo



    Arguments:
        id (ID): id
        rath (kuay.rath.KuayRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[GithubRepoFragment]"""
    return (await aexecute(Get_github_repoQuery, {"id": id}, rath=rath)).github_repo


def get_github_repo(id: ID, rath: KuayRath = None) -> Optional[GithubRepoFragment]:
    """get_github_repo



    Arguments:
        id (ID): id
        rath (kuay.rath.KuayRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[GithubRepoFragment]"""
    return execute(Get_github_repoQuery, {"id": id}, rath=rath).github_repo


async def asearch_githubrepo(
    search: str, rath: KuayRath = None
) -> Optional[List[Optional[Search_githubrepoQueryGithubrepos]]]:
    """search_githubrepo



    Arguments:
        search (str): search
        rath (kuay.rath.KuayRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[Search_githubrepoQueryGithubrepos]]]"""
    return (
        await aexecute(Search_githubrepoQuery, {"search": search}, rath=rath)
    ).github_repos


def search_githubrepo(
    search: str, rath: KuayRath = None
) -> Optional[List[Optional[Search_githubrepoQueryGithubrepos]]]:
    """search_githubrepo



    Arguments:
        search (str): search
        rath (kuay.rath.KuayRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[Search_githubrepoQueryGithubrepos]]]"""
    return execute(Search_githubrepoQuery, {"search": search}, rath=rath).github_repos
