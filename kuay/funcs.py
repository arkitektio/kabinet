from koil.helpers import unkoil_gen
from kuay.rath import KuayRath, current_kuay_rath
from koil import unkoil


def execute(operation, variables, rath: KuayRath = None):
    return unkoil(aexecute, operation, variables, rath)


async def aexecute(operation, variables, rath: KuayRath = None):
    rath = rath or current_kuay_rath.get()
    x = await rath.aquery(
        operation.Meta.document, operation.Arguments(**variables).dict(by_alias=True)
    )
    return operation(**x.data)


def subscribe(operation, variables, rath: KuayRath = None):
    return unkoil_gen(asubscribe, operation, variables, rath)


async def asubscribe(operation, variables, rath: KuayRath = None):
    rath = rath or current_kuay_rath.get()
    async for event in rath.asubscribe(
        operation.Meta.document, operation.Arguments(**variables).dict(by_alias=True)
    ):
        yield operation(**event.data)
