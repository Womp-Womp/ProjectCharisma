from dataclasses import dataclass, field
from typing import List

@dataclass
class Unit:
    """Represents a single unit type."""
    id: str = ""
    name: str = ""
    hp: int = 100
    movement: int = 5
    faction_id: str = ""
    abilities: List[str] = field(default_factory=list)


@dataclass
class Faction:
    """Represents a faction."""
    id: str = ""
    name: str = ""
    unit_ids: List[str] = field(default_factory=list)


@dataclass
class MapTile:
    """Represents a single tile on the map."""
    x: int = 0
    y: int = 0
    terrain_type: str = "space"
    unit_id: str = ""
