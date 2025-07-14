from dataclasses import dataclass, field
from typing import List

@dataclass
class Unit:
    id: str
    name: str
    hp: int
    attack: int
    defense: int

@dataclass
class Faction:
    id: str
    name: str
    units: List[str] = field(default_factory=list)

@dataclass
class MapTile:
    id: str
    walkable: bool = True

@dataclass
class GameMap:
    id: str
    name: str
    width: int
    height: int
    tiles: List[List[str]] = field(default_factory=list)
