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
