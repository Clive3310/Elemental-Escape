from src.constants import *
import arcade.gui
from pyglet.graphics import Batch

MAX_BUTTON_SIZE = (400, 300)
BUTTON_WIDTH = WINDOW_SIZE[0] // 2 if WINDOW_SIZE[0] // 2 <= MAX_BUTTON_SIZE[0] else MAX_BUTTON_SIZE[0]
BUTTON_HEIGHT = WINDOW_SIZE[1] // 7 if WINDOW_SIZE[1] // 7 <= MAX_BUTTON_SIZE[1] else MAX_BUTTON_SIZE[1]
BUTTON_MARGIN = BUTTON_HEIGHT // 4
Y_OFFSET_CENTER = BUTTON_HEIGHT + BUTTON_MARGIN


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = WINDOW_BASE_COLOR
        self.window.size = WINDOW_SIZE
        self.setup()

    def setup(self):
        self.UIman = arcade.gui.UIManager()

        x = WINDOW_SIZE[0] // 2 - BUTTON_WIDTH // 2
        y_center = WINDOW_SIZE[1] // 2 - Y_OFFSET_CENTER
        play_button = arcade.gui.UIFlatButton(x=x, y=y_center + BUTTON_HEIGHT // 2 + BUTTON_MARGIN,
                                              width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text="Play",
                                              style=BUTTON_STYLE)
        settings_button = arcade.gui.UIFlatButton(x=x, y=y_center - BUTTON_HEIGHT // 2,
                                                  width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text="Settings",
                                                  style=BUTTON_STYLE)
        exit_button = arcade.gui.UIFlatButton(x=x, y=y_center - BUTTON_HEIGHT // 2 - BUTTON_MARGIN - BUTTON_HEIGHT,
                                              width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text="Exit",
                                              style=BUTTON_STYLE)
        play_button.on_click = self.play
        settings_button.on_click = self.settings
        exit_button.on_click = self.exiting
        self.UIman.add(play_button)
        self.UIman.add(settings_button)
        self.UIman.add(exit_button)

        self.title_drop_batch = Batch()

    def on_show_view(self):
        self.UIman.enable()

    def on_hide_view(self):
        self.UIman.disable()

    def on_draw(self):
        self.clear()
        self.UIman.draw()

        title_drop = arcade.Text("Elemental Escape", WINDOW_SIZE[0] // 2 - TITLE_STYLE["font_size"] * 6,
                                 WINDOW_SIZE[1] // 2 + WINDOW_SIZE[1] // 4,
                                 **TITLE_STYLE, batch=self.title_drop_batch)
        self.title_drop_batch.draw()

    def play(self, _a):
        pass

    def settings(self, _a):
        pass

    def exiting(self, _a):
        arcade.exit()


if __name__ == "__main__":
    window = arcade.Window()
    view = MenuView()
    window.show_view(view)
    arcade.run()
