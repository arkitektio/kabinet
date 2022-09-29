from pydantic import Field
from fakts.fakts import Fakts
from herre.fakts.herre import FaktsHerre
from herre.herre import Herre
from koil.composition import Composition
from kuay.composition.kuay import Kuay


class KuayApp(Composition):
    fakts: Fakts = Field(default_factory=Fakts)
    herre: Herre = Field(default_factory=FaktsHerre)
    kuay: Kuay = Field(default_factory=Kuay)

    class Config:
        arbitrary_types_allowed = True
