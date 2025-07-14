from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict

from charisma_common.models import Unit, Faction, MapTile


@dataclass
class Player:
    """Represents a player in the game."""
    id: str
    name: str
    faction: Faction
    is_ai: bool = False


@dataclass
class GameState:
    """Represents the current state of the game."""
    units: Dict[str, Unit] = field(default_factory=dict)
    factions: Dict[str, Faction] = field(default_factory=dict)
    map_tiles: List[MapTile] = field(default_factory=list)
    players: List[Player] = field(default_factory=list)
    current_turn: int = 0


class State(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def on_enter(self):
        pass

    @abstractmethod
    def on_exit(self):
        pass

    @abstractmethod
    def on_update(self, delta_time):
        pass

    @abstractmethod
    def on_draw(self):
        pass
class MainMenuState(State):
    def on_enter(self):
        print("Entering Main Menu")

    def on_exit(self):
        print("Exiting Main Menu")

    def on_update(self, delta_time):
        pass

    def on_draw(self):
        pass
