""" Strucutre Registration

"""


from kuay.api.schema import GithubRepoFragment, aget_github_repo, Search_githubrepoQuery


try:
    from arkitekt.structures.default import get_default_structure_registry
    from arkitekt.widgets import SearchWidget

    structure_reg = get_default_structure_registry()
    structure_reg.register_as_structure(
        GithubRepoFragment,
        identifier="@port/githubrepo",
        expand=aget_github_repo,
        default_widget=SearchWidget(query=Search_githubrepoQuery.Meta.document),
    )

except ImportError:
    structure_reg = None
