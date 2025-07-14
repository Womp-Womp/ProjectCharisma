# This will be the main entry point for the Charisma Engine
import arcade
from engine.state import MainMenuState

class Game(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Charisma Engine")
        arcade.set_background_color(arcade.color.BLACK)
        self.current_state = None

    def setup(self):
        self.change_state(MainMenuState(self))

    def change_state(self, new_state):
        if self.current_state:
            self.current_state.on_exit()
        self.current_state = new_state
        self.current_state.on_enter()

    def on_draw(self):
        self.clear()
        if self.current_state:
            self.current_state.on_draw()

    def on_update(self, delta_time):
        if self.current_state:
            self.current_state.on_update(delta_time)

def main():
    window = Game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
