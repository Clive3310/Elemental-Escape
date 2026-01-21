from src.constants import *
import arcade.gui
from src.data_save_load import *

BUTTON_WIDTH = WINDOW_SIZE[0] // 2.5
BUTTON_HEIGHT = WINDOW_SIZE[1] // 5
BUTTON_MARGIN_X = WINDOW_SIZE[0] // 9
BUTTON_MARGIN_Y = BUTTON_HEIGHT // 4


class ChooseView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = WINDOW_MENU_COLOR
        if not self.window.fullscreen:
            self.window.size = WINDOW_SIZE
        self.setup()

    def setup(self):
        self.levels_data = dict()
        for i in range(1, 7):
            self.levels_data[i] = load_level_data(i)

        self.UIman = arcade.gui.UIManager()

        x_left = WINDOW_SIZE[0] // 2 - BUTTON_WIDTH - BUTTON_MARGIN_X // 2
        x_right = WINDOW_SIZE[0] // 2 + BUTTON_MARGIN_X // 2

        for i in range(1, 4):
            f_stars = ("★ " * self.levels_data[i]["Stars"] + "☆ " * (3 - self.levels_data[i]["Stars"])).strip()
            s_stars = ("★ " * self.levels_data[i + 3]["Stars"] + "☆ " * (3 - self.levels_data[i + 3]["Stars"])).strip()
            y = WINDOW_SIZE[1] - (BUTTON_HEIGHT + BUTTON_MARGIN_Y) * i
            lv_button_left = arcade.gui.UIFlatButton(x=x_left, y=y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                                     text=f"Level {i} {f_stars}",
                                                     style=BUTTON_STYLE)
            lv_button_right = arcade.gui.UIFlatButton(x=x_right, y=y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                                      text=f"Level {i + 3} {s_stars}",
                                                      style=BUTTON_STYLE)
            lv_button_left.on_click = lambda _a, ind=i: self.load_level_view(_a, ind=ind)
            lv_button_right.on_click = lambda _a, ind=i + 3: self.load_level_view(_a, ind=ind)
            self.UIman.add(lv_button_left)
            self.UIman.add(lv_button_right)

        back_button = arcade.gui.UIFlatButton(x=WINDOW_SIZE[0] // 2 - BUTTON_WIDTH, y=BUTTON_HEIGHT // 4,
                                              width=BUTTON_WIDTH * 2, height=BUTTON_HEIGHT // 2, text="<------",
                                              style=BUTTON_STYLE)
        back_button.on_click = self.return_to_menu
        self.UIman.add(back_button)

    def on_show_view(self):
        self.UIman.enable()

    def on_hide_view(self):
        self.UIman.disable()

    def on_draw(self):
        self.clear()
        self.UIman.draw()

    def return_to_menu(self, _a):
        from src.menu_view import MenuView
        view = MenuView()
        self.window.show_view(view)

    def load_level_view(self, _a, ind: int = 1):
        from src.level_view import LevelView
        view = LevelView(ind)
        self.window.show_view(view)


if __name__ == "__main__":
    window = arcade.Window()
    view = ChooseView()
    window.show_view(view)
    arcade.run()
