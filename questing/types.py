from pycdr import cdr
from enum import Enum


class FishType(Enum):
    Shimmering = 0
    Matte = 1
    Metallic = 2


@cdr(typename="__main__::CuriousFish")
class CuriousFish:
    fish_type: FishType
    dorsal_fins: int
    fish_name: str


@cdr(typename="__main__::Island")
class Island:
    X: float
    Y: float
    size: float
    name: str

@cdr(typename="__main__::Wave")
class Wave:
    height: int
    volume: float