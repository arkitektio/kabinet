""" The Kluster (Client) Composition packages"""
from koil.composition import Composition
from .rath import KabinetRath


class Kabinet(Composition):
    """The Kabinet Composition

    This composition is the main entry point for the kluster client.
    and is used to build a client for a kluster instance, that can be
    used to execute graphql operations and retrieve the dask client
    from a connected dask gateway trough the repository.

    """

    rath: KabinetRath
