from pydantic import BaseModel, Field
from kabinet.funcs import subscribe, asubscribe, execute, aexecute
from typing import List, Optional, AsyncIterator, Literal, Iterator, Tuple
from kabinet.rath import KabinetRath
from rath.scalars import ID
from enum import Enum


class PortKind(str, Enum):
    INT = "INT"
    STRING = "STRING"
    STRUCTURE = "STRUCTURE"
    LIST = "LIST"
    BOOL = "BOOL"
    DICT = "DICT"
    FLOAT = "FLOAT"
    DATE = "DATE"
    UNION = "UNION"


class ContainerType(str, Enum):
    """The state of a dask cluster"""

    APPTAINER = "APPTAINER"
    DOCKER = "DOCKER"


class PodStatus(str, Enum):
    """The state of a dask cluster"""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"
    UNKOWN = "UNKOWN"


class EnvironmentInput(BaseModel):
    """Which environment do you want to match against?"""

    container_type: ContainerType = Field(alias="containerType")

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        allow_population_by_field_name = True
        use_enum_values = True


class GithubRepoFragment(BaseModel):
    typename: Optional[Literal["GithubRepo"]] = Field(alias="__typename", exclude=True)
    user: str
    branch: str
    repo: str
    id: ID

    class Config:
        """A config class"""

        frozen = True


class ListFlavourFragmentDeployments(BaseModel):
    """A user of the bridge server. Maps to an authentikate user"""

    typename: Optional[Literal["Deployment"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class ListFlavourFragment(BaseModel):
    typename: Optional[Literal["Flavour"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    deployments: Tuple[ListFlavourFragmentDeployments, ...]

    class Config:
        """A config class"""

        frozen = True


class FlavourFragmentDeployments(BaseModel):
    """A user of the bridge server. Maps to an authentikate user"""

    typename: Optional[Literal["Deployment"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class FlavourFragment(BaseModel):
    typename: Optional[Literal["Flavour"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    deployments: Tuple[FlavourFragmentDeployments, ...]
    image: str

    class Config:
        """A config class"""

        frozen = True


class DeploymentFragment(BaseModel):
    typename: Optional[Literal["Deployment"]] = Field(alias="__typename", exclude=True)
    id: ID
    backend: "BackendFragment"

    class Config:
        """A config class"""

        frozen = True


class DefinitionFragmentArgs(BaseModel):
    typename: Optional[Literal["Port"]] = Field(alias="__typename", exclude=True)
    kind: PortKind

    class Config:
        """A config class"""

        frozen = True


class DefinitionFragment(BaseModel):
    typename: Optional[Literal["Definition"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    "The cleartext name of this Node"
    hash: ID
    "The hash of the Node (completely unique)"
    description: Optional[str]
    "A description for the Node"
    args: Tuple[DefinitionFragmentArgs, ...]
    "Inputs for this Node"

    class Config:
        """A config class"""

        frozen = True


class ListDefinitionFragment(BaseModel):
    typename: Optional[Literal["Definition"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    "The cleartext name of this Node"
    hash: ID
    "The hash of the Node (completely unique)"
    description: Optional[str]
    "A description for the Node"

    class Config:
        """A config class"""

        frozen = True


class PodFragment(BaseModel):
    typename: Optional[Literal["Pod"]] = Field(alias="__typename", exclude=True)
    pod_id: str = Field(alias="podId")
    status: PodStatus
    backend: "BackendFragment"

    class Config:
        """A config class"""

        frozen = True


class ListPodFragment(BaseModel):
    typename: Optional[Literal["Pod"]] = Field(alias="__typename", exclude=True)
    id: ID
    pod_id: str = Field(alias="podId")

    class Config:
        """A config class"""

        frozen = True


class ReleaseFragmentApp(BaseModel):
    """A user of the bridge server. Maps to an authentikate user"""

    typename: Optional[Literal["App"]] = Field(alias="__typename", exclude=True)
    identifier: str

    class Config:
        """A config class"""

        frozen = True


class ReleaseFragmentDeployments(BaseModel):
    """A user of the bridge server. Maps to an authentikate user"""

    typename: Optional[Literal["Deployment"]] = Field(alias="__typename", exclude=True)
    id: ID
    flavour: ListFlavourFragment

    class Config:
        """A config class"""

        frozen = True


class ReleaseFragment(BaseModel):
    typename: Optional[Literal["Release"]] = Field(alias="__typename", exclude=True)
    id: ID
    version: str
    app: ReleaseFragmentApp
    scopes: Tuple[str, ...]
    deployments: Tuple[ReleaseFragmentDeployments, ...]
    "Is this release deployed"
    colour: str
    "Is this release deployed"
    description: str
    "Is this release deployed"

    class Config:
        """A config class"""

        frozen = True


class ListReleaseFragmentApp(BaseModel):
    """A user of the bridge server. Maps to an authentikate user"""

    typename: Optional[Literal["App"]] = Field(alias="__typename", exclude=True)
    identifier: str

    class Config:
        """A config class"""

        frozen = True


class ListReleaseFragment(BaseModel):
    typename: Optional[Literal["Release"]] = Field(alias="__typename", exclude=True)
    id: ID
    version: str
    app: ListReleaseFragmentApp
    installed: bool
    "Is this release deployed"
    scopes: Tuple[str, ...]
    flavours: Tuple[ListFlavourFragment, ...]
    colour: str
    "Is this release deployed"
    description: str
    "Is this release deployed"

    class Config:
        """A config class"""

        frozen = True


class PodUpdateMessageFragment(BaseModel):
    typename: Optional[Literal["PodUpdateMessage"]] = Field(
        alias="__typename", exclude=True
    )
    id: str
    status: str
    progress: Optional[int]

    class Config:
        """A config class"""

        frozen = True


class BackendFragmentUser(BaseModel):
    """A user of the bridge server. Maps to an authentikate user"""

    typename: Optional[Literal["User"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class BackendFragmentClient(BaseModel):
    """A user of the bridge server. Maps to an authentikate user"""

    typename: Optional[Literal["Client"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class BackendFragment(BaseModel):
    typename: Optional[Literal["Backend"]] = Field(alias="__typename", exclude=True)
    user: BackendFragmentUser
    client: BackendFragmentClient

    class Config:
        """A config class"""

        frozen = True


class PodsSubscription(BaseModel):
    pods: PodUpdateMessageFragment
    "Create a new dask cluster on a bridge server"

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment PodUpdateMessage on PodUpdateMessage {\n  id\n  status\n  progress\n}\n\nsubscription Pods {\n  pods {\n    ...PodUpdateMessage\n  }\n}"


class CreateGithubRepoMutation(BaseModel):
    create_github_repo: GithubRepoFragment = Field(alias="createGithubRepo")
    "Create a new Github repository on a bridge server"

    class Arguments(BaseModel):
        name: str
        branch: str
        user: str
        repo: str

    class Meta:
        document = "fragment GithubRepo on GithubRepo {\n  user\n  branch\n  repo\n  id\n}\n\nmutation CreateGithubRepo($name: String!, $branch: String!, $user: String!, $repo: String!) {\n  createGithubRepo(\n    input: {branch: $branch, user: $user, repo: $repo, name: $name}\n  ) {\n    ...GithubRepo\n  }\n}"


class CreateDeploymentMutation(BaseModel):
    create_deployment: DeploymentFragment = Field(alias="createDeployment")
    "Create a new dask cluster on a bridge server"

    class Arguments(BaseModel):
        flavour: ID
        instance_id: ID = Field(alias="instanceId")

    class Meta:
        document = "fragment Backend on Backend {\n  user {\n    id\n  }\n  client {\n    id\n  }\n}\n\nfragment Deployment on Deployment {\n  id\n  backend {\n    ...Backend\n  }\n}\n\nmutation CreateDeployment($flavour: ID!, $instanceId: ID!) {\n  createDeployment(input: {flavour: $flavour, instanceId: $instanceId}) {\n    ...Deployment\n  }\n}"


class CreatePodMutation(BaseModel):
    create_pod: PodFragment = Field(alias="createPod")
    "Create a new dask cluster on a bridge server"

    class Arguments(BaseModel):
        deployment: ID
        instance_id: str = Field(alias="instanceId")

    class Meta:
        document = "fragment Backend on Backend {\n  user {\n    id\n  }\n  client {\n    id\n  }\n}\n\nfragment Pod on Pod {\n  podId\n  status\n  backend {\n    ...Backend\n  }\n}\n\nmutation CreatePod($deployment: ID!, $instanceId: String!) {\n  createPod(input: {deployment: $deployment, instanceId: $instanceId}) {\n    ...Pod\n  }\n}"


class GetGithubRepoQuery(BaseModel):
    github_repo: GithubRepoFragment = Field(alias="githubRepo")
    "Return all dask clusters"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment GithubRepo on GithubRepo {\n  user\n  branch\n  repo\n  id\n}\n\nquery GetGithubRepo($id: ID!) {\n  githubRepo(id: $id) {\n    ...GithubRepo\n  }\n}"


class SearchGithubReposQueryOptions(BaseModel):
    """A user of the bridge server. Maps to an authentikate user"""

    typename: Optional[Literal["GithubRepo"]] = Field(alias="__typename", exclude=True)
    value: ID
    label: str

    class Config:
        """A config class"""

        frozen = True


class SearchGithubReposQuery(BaseModel):
    options: Tuple[SearchGithubReposQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchGithubRepos($search: String, $values: [ID!]) {\n  options: githubRepos(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n  }\n}"


class ListFlavourQuery(BaseModel):
    flavours: Tuple[ListFlavourFragment, ...]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment ListFlavour on Flavour {\n  id\n  name\n  deployments {\n    id\n  }\n}\n\nquery ListFlavour {\n  flavours {\n    ...ListFlavour\n  }\n}"


class GetFlavourQuery(BaseModel):
    flavour: FlavourFragment
    "Return all dask clusters"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Flavour on Flavour {\n  id\n  name\n  deployments {\n    id\n  }\n  image\n}\n\nquery GetFlavour($id: ID!) {\n  flavour(id: $id) {\n    ...Flavour\n  }\n}"


class BestFlavourForQuery(BaseModel):
    best_flavour: FlavourFragment = Field(alias="bestFlavour")
    "Return the currently logged in user"

    class Arguments(BaseModel):
        id: ID
        environment: EnvironmentInput

    class Meta:
        document = "fragment Flavour on Flavour {\n  id\n  name\n  deployments {\n    id\n  }\n  image\n}\n\nquery BestFlavourFor($id: ID!, $environment: EnvironmentInput!) {\n  bestFlavour(release: $id, environment: $environment) {\n    ...Flavour\n  }\n}"


class ListPodsQuery(BaseModel):
    pods: Tuple[ListPodFragment, ...]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment ListPod on Pod {\n  id\n  podId\n}\n\nquery ListPods {\n  pods {\n    ...ListPod\n  }\n}"


class ListReleasesQuery(BaseModel):
    releases: Tuple[ListReleaseFragment, ...]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment ListFlavour on Flavour {\n  id\n  name\n  deployments {\n    id\n  }\n}\n\nfragment ListRelease on Release {\n  id\n  version\n  app {\n    identifier\n  }\n  installed\n  scopes\n  flavours {\n    ...ListFlavour\n  }\n  colour\n  description\n}\n\nquery ListReleases {\n  releases {\n    ...ListRelease\n  }\n}"


class GetReleaseQuery(BaseModel):
    release: ReleaseFragment
    "Return all dask clusters"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment ListFlavour on Flavour {\n  id\n  name\n  deployments {\n    id\n  }\n}\n\nfragment Release on Release {\n  id\n  version\n  app {\n    identifier\n  }\n  scopes\n  deployments {\n    id\n    flavour {\n      ...ListFlavour\n    }\n  }\n  colour\n  description\n}\n\nquery GetRelease($id: ID!) {\n  release(id: $id) {\n    ...Release\n  }\n}"


class ListDefinitionsQuery(BaseModel):
    definitions: Tuple[ListDefinitionFragment, ...]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment ListDefinition on Definition {\n  id\n  name\n  hash\n  description\n}\n\nquery ListDefinitions {\n  definitions {\n    ...ListDefinition\n  }\n}"


class GetDefinitionQuery(BaseModel):
    definition: DefinitionFragment
    "Return all dask clusters"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Definition on Definition {\n  id\n  name\n  hash\n  description\n  args {\n    kind\n  }\n}\n\nquery GetDefinition($id: ID!) {\n  definition(id: $id) {\n    ...Definition\n  }\n}"


async def apods(
    rath: Optional[KabinetRath] = None,
) -> AsyncIterator[PodUpdateMessageFragment]:
    """Pods


     pods: An update on a pod


    Arguments:
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        PodUpdateMessageFragment"""
    async for event in asubscribe(PodsSubscription, {}, rath=rath):
        yield event.pods


def pods(rath: Optional[KabinetRath] = None) -> Iterator[PodUpdateMessageFragment]:
    """Pods


     pods: An update on a pod


    Arguments:
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        PodUpdateMessageFragment"""
    for event in subscribe(PodsSubscription, {}, rath=rath):
        yield event.pods


async def acreate_github_repo(
    name: str, branch: str, user: str, repo: str, rath: Optional[KabinetRath] = None
) -> GithubRepoFragment:
    """CreateGithubRepo


     createGithubRepo: A user of the bridge server. Maps to an authentikate user


    Arguments:
        name (str): name
        branch (str): branch
        user (str): user
        repo (str): repo
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        GithubRepoFragment"""
    return (
        await aexecute(
            CreateGithubRepoMutation,
            {"name": name, "branch": branch, "user": user, "repo": repo},
            rath=rath,
        )
    ).create_github_repo


def create_github_repo(
    name: str, branch: str, user: str, repo: str, rath: Optional[KabinetRath] = None
) -> GithubRepoFragment:
    """CreateGithubRepo


     createGithubRepo: A user of the bridge server. Maps to an authentikate user


    Arguments:
        name (str): name
        branch (str): branch
        user (str): user
        repo (str): repo
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        GithubRepoFragment"""
    return execute(
        CreateGithubRepoMutation,
        {"name": name, "branch": branch, "user": user, "repo": repo},
        rath=rath,
    ).create_github_repo


async def acreate_deployment(
    flavour: ID, instance_id: ID, rath: Optional[KabinetRath] = None
) -> DeploymentFragment:
    """CreateDeployment


     createDeployment: A user of the bridge server. Maps to an authentikate user


    Arguments:
        flavour (ID): flavour
        instance_id (ID): instanceId
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        DeploymentFragment"""
    return (
        await aexecute(
            CreateDeploymentMutation,
            {"flavour": flavour, "instanceId": instance_id},
            rath=rath,
        )
    ).create_deployment


def create_deployment(
    flavour: ID, instance_id: ID, rath: Optional[KabinetRath] = None
) -> DeploymentFragment:
    """CreateDeployment


     createDeployment: A user of the bridge server. Maps to an authentikate user


    Arguments:
        flavour (ID): flavour
        instance_id (ID): instanceId
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        DeploymentFragment"""
    return execute(
        CreateDeploymentMutation,
        {"flavour": flavour, "instanceId": instance_id},
        rath=rath,
    ).create_deployment


async def acreate_pod(
    deployment: ID, instance_id: str, rath: Optional[KabinetRath] = None
) -> PodFragment:
    """CreatePod


     createPod: A user of the bridge server. Maps to an authentikate user


    Arguments:
        deployment (ID): deployment
        instance_id (str): instanceId
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        PodFragment"""
    return (
        await aexecute(
            CreatePodMutation,
            {"deployment": deployment, "instanceId": instance_id},
            rath=rath,
        )
    ).create_pod


def create_pod(
    deployment: ID, instance_id: str, rath: Optional[KabinetRath] = None
) -> PodFragment:
    """CreatePod


     createPod: A user of the bridge server. Maps to an authentikate user


    Arguments:
        deployment (ID): deployment
        instance_id (str): instanceId
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        PodFragment"""
    return execute(
        CreatePodMutation,
        {"deployment": deployment, "instanceId": instance_id},
        rath=rath,
    ).create_pod


async def aget_github_repo(
    id: ID, rath: Optional[KabinetRath] = None
) -> GithubRepoFragment:
    """GetGithubRepo


     githubRepo: A user of the bridge server. Maps to an authentikate user


    Arguments:
        id (ID): id
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        GithubRepoFragment"""
    return (await aexecute(GetGithubRepoQuery, {"id": id}, rath=rath)).github_repo


def get_github_repo(id: ID, rath: Optional[KabinetRath] = None) -> GithubRepoFragment:
    """GetGithubRepo


     githubRepo: A user of the bridge server. Maps to an authentikate user


    Arguments:
        id (ID): id
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        GithubRepoFragment"""
    return execute(GetGithubRepoQuery, {"id": id}, rath=rath).github_repo


async def asearch_github_repos(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KabinetRath] = None,
) -> List[SearchGithubReposQueryOptions]:
    """SearchGithubRepos


     options: A user of the bridge server. Maps to an authentikate user


    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        List[SearchGithubReposQueryGithubrepos]"""
    return (
        await aexecute(
            SearchGithubReposQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_github_repos(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KabinetRath] = None,
) -> List[SearchGithubReposQueryOptions]:
    """SearchGithubRepos


     options: A user of the bridge server. Maps to an authentikate user


    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        List[SearchGithubReposQueryGithubrepos]"""
    return execute(
        SearchGithubReposQuery, {"search": search, "values": values}, rath=rath
    ).options


async def alist_flavour(
    rath: Optional[KabinetRath] = None,
) -> List[ListFlavourFragment]:
    """ListFlavour


     flavours: A user of the bridge server. Maps to an authentikate user


    Arguments:
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        List[ListFlavourFragment]"""
    return (await aexecute(ListFlavourQuery, {}, rath=rath)).flavours


def list_flavour(rath: Optional[KabinetRath] = None) -> List[ListFlavourFragment]:
    """ListFlavour


     flavours: A user of the bridge server. Maps to an authentikate user


    Arguments:
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        List[ListFlavourFragment]"""
    return execute(ListFlavourQuery, {}, rath=rath).flavours


async def aget_flavour(id: ID, rath: Optional[KabinetRath] = None) -> FlavourFragment:
    """GetFlavour


     flavour: A user of the bridge server. Maps to an authentikate user


    Arguments:
        id (ID): id
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        FlavourFragment"""
    return (await aexecute(GetFlavourQuery, {"id": id}, rath=rath)).flavour


def get_flavour(id: ID, rath: Optional[KabinetRath] = None) -> FlavourFragment:
    """GetFlavour


     flavour: A user of the bridge server. Maps to an authentikate user


    Arguments:
        id (ID): id
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        FlavourFragment"""
    return execute(GetFlavourQuery, {"id": id}, rath=rath).flavour


async def abest_flavour_for(
    id: ID, environment: EnvironmentInput, rath: Optional[KabinetRath] = None
) -> FlavourFragment:
    """BestFlavourFor


     bestFlavour: A user of the bridge server. Maps to an authentikate user


    Arguments:
        id (ID): id
        environment (EnvironmentInput): environment
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        FlavourFragment"""
    return (
        await aexecute(
            BestFlavourForQuery, {"id": id, "environment": environment}, rath=rath
        )
    ).best_flavour


def best_flavour_for(
    id: ID, environment: EnvironmentInput, rath: Optional[KabinetRath] = None
) -> FlavourFragment:
    """BestFlavourFor


     bestFlavour: A user of the bridge server. Maps to an authentikate user


    Arguments:
        id (ID): id
        environment (EnvironmentInput): environment
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        FlavourFragment"""
    return execute(
        BestFlavourForQuery, {"id": id, "environment": environment}, rath=rath
    ).best_flavour


async def alist_pods(rath: Optional[KabinetRath] = None) -> List[ListPodFragment]:
    """ListPods


     pods: A user of the bridge server. Maps to an authentikate user


    Arguments:
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        List[ListPodFragment]"""
    return (await aexecute(ListPodsQuery, {}, rath=rath)).pods


def list_pods(rath: Optional[KabinetRath] = None) -> List[ListPodFragment]:
    """ListPods


     pods: A user of the bridge server. Maps to an authentikate user


    Arguments:
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        List[ListPodFragment]"""
    return execute(ListPodsQuery, {}, rath=rath).pods


async def alist_releases(
    rath: Optional[KabinetRath] = None,
) -> List[ListReleaseFragment]:
    """ListReleases


     releases: A user of the bridge server. Maps to an authentikate user


    Arguments:
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        List[ListReleaseFragment]"""
    return (await aexecute(ListReleasesQuery, {}, rath=rath)).releases


def list_releases(rath: Optional[KabinetRath] = None) -> List[ListReleaseFragment]:
    """ListReleases


     releases: A user of the bridge server. Maps to an authentikate user


    Arguments:
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        List[ListReleaseFragment]"""
    return execute(ListReleasesQuery, {}, rath=rath).releases


async def aget_release(id: ID, rath: Optional[KabinetRath] = None) -> ReleaseFragment:
    """GetRelease


     release: A user of the bridge server. Maps to an authentikate user


    Arguments:
        id (ID): id
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        ReleaseFragment"""
    return (await aexecute(GetReleaseQuery, {"id": id}, rath=rath)).release


def get_release(id: ID, rath: Optional[KabinetRath] = None) -> ReleaseFragment:
    """GetRelease


     release: A user of the bridge server. Maps to an authentikate user


    Arguments:
        id (ID): id
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        ReleaseFragment"""
    return execute(GetReleaseQuery, {"id": id}, rath=rath).release


async def alist_definitions(
    rath: Optional[KabinetRath] = None,
) -> List[ListDefinitionFragment]:
    """ListDefinitions


     definitions: Nodes are abstraction of RPC Tasks. They provide a common API to deal with creating tasks.

    See online Documentation


    Arguments:
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        List[ListDefinitionFragment]"""
    return (await aexecute(ListDefinitionsQuery, {}, rath=rath)).definitions


def list_definitions(
    rath: Optional[KabinetRath] = None,
) -> List[ListDefinitionFragment]:
    """ListDefinitions


     definitions: Nodes are abstraction of RPC Tasks. They provide a common API to deal with creating tasks.

    See online Documentation


    Arguments:
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        List[ListDefinitionFragment]"""
    return execute(ListDefinitionsQuery, {}, rath=rath).definitions


async def aget_definition(
    id: ID, rath: Optional[KabinetRath] = None
) -> DefinitionFragment:
    """GetDefinition


     definition: Nodes are abstraction of RPC Tasks. They provide a common API to deal with creating tasks.

    See online Documentation


    Arguments:
        id (ID): id
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        DefinitionFragment"""
    return (await aexecute(GetDefinitionQuery, {"id": id}, rath=rath)).definition


def get_definition(id: ID, rath: Optional[KabinetRath] = None) -> DefinitionFragment:
    """GetDefinition


     definition: Nodes are abstraction of RPC Tasks. They provide a common API to deal with creating tasks.

    See online Documentation


    Arguments:
        id (ID): id
        rath (kabinet.rath.KabinetRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        DefinitionFragment"""
    return execute(GetDefinitionQuery, {"id": id}, rath=rath).definition


DeploymentFragment.update_forward_refs()
PodFragment.update_forward_refs()
