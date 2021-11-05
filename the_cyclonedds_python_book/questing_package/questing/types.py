from cyclonedds.idl import IdlStruct
from dataclasses import dataclass
from enum import Enum


class FishType(Enum):
    Shimmering = 0
    Matte = 1
    Metallic = 2


@dataclass
class CuriousFish(typename="CuriousFish"):
    fish_type: FishType
    dorsal_fins: int
    fish_name: str


@dataclass
class Island(typename="Island"):
    X: float
    Y: float
    size: float
    name: str


@dataclass
class Wave(typename="Wave"):
    height: int
    volume: float
