"""What a kabinet app asks of whoever called it.

An app that needs something only a person can give finds it among its callers (rekuest's
``callerOf`` filter) by what the action does, not by its name. These are the demands both
sides agree on: the asking app looks one up, and the app answering it (orkestrator) declares
an action whose ports match.
"""

from arkitekt_spec.actions import ActionDemandInput, PortKind, PortMatchInput

RELEASE = "@kabinet/release"
APPROVAL = "@kabinet/approval"

#: Ask a person to approve a release for a deployer: takes the release and the deployer's app
#: identifier (``agent``, what the approval names), returns the approval they made.
REQUEST_APPROVAL = ActionDemandInput(
    arg_matches=(
        PortMatchInput(at=0, kind=PortKind.STRUCTURE, identifier=RELEASE),
        PortMatchInput(at=1, key="agent", kind=PortKind.STRING),
    ),
    return_matches=(PortMatchInput(at=0, kind=PortKind.STRUCTURE, identifier=APPROVAL),),
    force_arg_length=2,
    force_return_length=1,
)
