from src.constants import *
import arcade
import arcade.gui
from pyglet.graphics import Batch

MAX_BUTTON_SIZE = (400, 300)
BUTTON_WIDTH = WINDOW_SIZE[0] // 2 if WINDOW_SIZE[0] // 2 <= MAX_BUTTON_SIZE[0] else MAX_BUTTON_SIZE[0]
BUTTON_HEIGHT = WINDOW_SIZE[1] // 7 if WINDOW_SIZE[1] // 7 <= MAX_BUTTON_SIZE[1] else MAX_BUTTON_SIZE[1]
BUTTON_MARGIN = BUTTON_HEIGHT // 4


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = WINDOW_MENU_COLOR
        self.ui_manager = arcade.gui.UIManager()

        self.title_batch = Batch()
        self.title_text = None

        if not self.window.fullscreen:
            self.window.size = WINDOW_SIZE
        self.setup()

    def setup(self):
        self.ui_manager.enable()
        self.ui_manager.clear()

        anchor_layout = arcade.gui.UIAnchorLayout()
        v_box = arcade.gui.UIBoxLayout(space_between=BUTTON_MARGIN)

        play_button = arcade.gui.UIFlatButton(text="Play", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, style=BUTTON_STYLE)
        play_button.on_click = self.play
        v_box.add(play_button)

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                                  style=BUTTON_STYLE)
        settings_button.on_click = self.settings
        v_box.add(settings_button)

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, style=BUTTON_STYLE)
        exit_button.on_click = self.exiting
        v_box.add(exit_button)

        anchor_layout.add(child=v_box, anchor_x="center_x", anchor_y="center_y", align_y=-30)
        self.ui_manager.add(anchor_layout)

        text_y = self.window.height / 2 + WINDOW_SIZE[1] // 4

        self.title_text = arcade.Text(
            "Elemental Escape",
            self.window.width / 2,
            text_y,
            anchor_x="center",
            **TITLE_STYLE,
            batch=self.title_batch
        )

    def on_show_view(self):
        self.ui_manager.enable()

    def on_hide_view(self):
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()

        self.title_batch.draw()

        self.ui_manager.draw()

    def play(self, _a):
        from src.lv_choose_view import ChooseView
        view = ChooseView()
        self.window.show_view(view)

    def settings(self, _a):
        from src.settings_view import SettingsView
        view = SettingsView()
        self.window.show_view(view)

    def exiting(self, _a):
        arcade.exit()


if __name__ == "__main__":
    window = arcade.Window()
    view = MenuView()
    window.show_view(view)
    arcade.run()
