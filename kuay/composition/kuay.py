from kuay.rath import KuayRath
from koil.composition import Composition
from pydantic import Field


class Kuay(Composition):
    rath: KuayRath = Field(default_factory=KuayRath)
