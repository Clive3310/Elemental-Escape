import arcade.gui
import json
import pathlib
from src.constants import *

MAX_BUTTON_SIZE = (400, 300)
BUTTON_WIDTH = WINDOW_SIZE[0] // 2 if WINDOW_SIZE[0] // 2 <= MAX_BUTTON_SIZE[0] else MAX_BUTTON_SIZE[0]
BUTTON_HEIGHT = WINDOW_SIZE[1] // 7 if WINDOW_SIZE[1] // 7 <= MAX_BUTTON_SIZE[1] else MAX_BUTTON_SIZE[1]
BUTTON_MARGIN = BUTTON_HEIGHT // 4


class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = WINDOW_MENU_COLOR
        self.UIman = arcade.gui.UIManager()
        self.title_text = None
        self.setup()

    def setup(self):
        self.UIman.enable()
        self.UIman.clear()

        self.title_text = arcade.Text(
            "Settings",
            self.window.width / 2,
            self.window.height / 2 + WINDOW_SIZE[1] // 4,
            anchor_x="center",
            **TITLE_STYLE
        )

        anchor_layout = arcade.gui.UIAnchorLayout()

        v_box = arcade.gui.UIBoxLayout(space_between=BUTTON_MARGIN)

        current_state = self.window.fullscreen
        btn_text = "Fullscreen: ON" if current_state else "Fullscreen: OFF"

        self.btn_fullscreen = arcade.gui.UIFlatButton(
            text=btn_text,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            style=BUTTON_STYLE
        )
        self.btn_fullscreen.on_click = self.on_click_fullscreen
        v_box.add(self.btn_fullscreen)

        btn_back = arcade.gui.UIFlatButton(
            text="Back",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            style=BUTTON_STYLE
        )
        btn_back.on_click = self.on_click_back
        v_box.add(btn_back)

        anchor_layout.add(child=v_box, anchor_x="center_x", anchor_y="center_y")
        self.UIman.add(anchor_layout)

    def on_click_fullscreen(self, event):
        self.window.set_fullscreen(not self.window.fullscreen)

        if self.window.fullscreen:
            self.btn_fullscreen.text = "Fullscreen: ON"
        else:
            self.btn_fullscreen.text = "Fullscreen: OFF"
            self.window.set_size(int(WINDOW_SIZE[0]), int(WINDOW_SIZE[1]))

        self.title_text.x = self.window.width / 2
        self.title_text.y = self.window.height / 2 + WINDOW_SIZE[1] // 4

        path = pathlib.Path(__file__).parent / "settings.json"

        try:
            data = {}
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)

            data["fullscreen"] = self.window.fullscreen

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    def on_click_back(self, event):
        from src.menu_view import MenuView
        view = MenuView()
        self.window.show_view(view)

    def on_show_view(self):
        self.UIman.enable()

    def on_hide_view(self):
        self.UIman.disable()

    def on_draw(self):
        self.clear()
        self.UIman.draw()
        if self.title_text:
            self.title_text.draw()
