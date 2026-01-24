import arcade.gui

from src.data_save_load import *

BUTTON_WIDTH = WINDOW_SIZE[0] // 2.5
BUTTON_HEIGHT = WINDOW_SIZE[1] // 7
BUTTON_MARGIN_X = WINDOW_SIZE[0] // 9
BUTTON_MARGIN_Y = BUTTON_HEIGHT // 3


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
        self.UIman.enable()
        self.UIman.clear()

        anchor_layout = arcade.gui.UIAnchorLayout()
        title_label = arcade.gui.UILabel(
            text="Choose Level",
            font_size=TITLE_STYLE["font_size"],
            font_name=TITLE_STYLE["font_name"][0],
            text_color=TITLE_STYLE["color"],
            bold=TITLE_STYLE["bold"]
        )

        main_vbox = arcade.gui.UIBoxLayout(space_between=BUTTON_MARGIN_Y, vertical=True)

        for i in range(1, 4):
            hbox = arcade.gui.UIBoxLayout(space_between=BUTTON_MARGIN_X, vertical=False)

            f_stars = ("★ " * self.levels_data[i]["Stars"] + "☆ " * (3 - self.levels_data[i]["Stars"])).strip()
            lv_button_left = arcade.gui.UIFlatButton(
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                text=f"Level {i}\n{f_stars}",
                style=BUTTON_STYLE
            )
            lv_button_left.on_click = lambda _a, ind=i: self.load_level_view(_a, ind=ind)
            hbox.add(lv_button_left)

            s_stars = ("★ " * self.levels_data[i + 3]["Stars"] + "☆ " * (3 - self.levels_data[i + 3]["Stars"])).strip()
            lv_button_right = arcade.gui.UIFlatButton(
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                text=f"Level {i + 3}\n{s_stars}",
                style=BUTTON_STYLE
            )
            lv_button_right.on_click = lambda _a, ind=i + 3: self.load_level_view(_a, ind=ind)
            hbox.add(lv_button_right)

            main_vbox.add(hbox)

        back_button = arcade.gui.UIFlatButton(
            width=BUTTON_WIDTH * 2 + BUTTON_MARGIN_X,
            height=BUTTON_HEIGHT,
            text="<-- Back",
            style=BUTTON_STYLE
        )
        back_button.on_click = self.return_to_menu

        anchor_layout.add(child=title_label, anchor_x="center_x", anchor_y="top", align_y=-30)
        anchor_layout.add(child=main_vbox, anchor_x="center_x", anchor_y="center_y", align_y=20)  # Сдвинул вверх
        anchor_layout.add(child=back_button, anchor_x="center_x", anchor_y="bottom", align_y=30)

        self.UIman.add(anchor_layout)

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

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.return_to_menu(None)
