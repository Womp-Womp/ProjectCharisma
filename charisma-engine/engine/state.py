from abc import ABC, abstractmethod

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
