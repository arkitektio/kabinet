from .app import KuayApp
from arkitekt.app import ArkitektApp


class ConnectedApp(KuayApp, ArkitektApp):
    """A connected app composed
    of both a Mikro App and a Arkitekt App.
    """
