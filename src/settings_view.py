import json
import pathlib

import arcade.gui

from src.constants import *

MAX_BUTTON_SIZE = (400, 300)
BUTTON_WIDTH = WINDOW_SIZE[0] // 2 if WINDOW_SIZE[0] // 2 <= MAX_BUTTON_SIZE[0] else MAX_BUTTON_SIZE[0]
BUTTON_HEIGHT = WINDOW_SIZE[1] // 10
BUTTON_MARGIN = BUTTON_HEIGHT // 4
CONTROL_BUTTON_WIDTH = BUTTON_WIDTH // 3.2
CONTROL_BUTTON_HEIGHT = BUTTON_HEIGHT

ALLOWED_KEYS = {
    97: "A", 98: "B", 99: "C", 100: "D", 101: "E", 102: "F",
    103: "G", 104: "H", 105: "I", 106: "J", 107: "K", 108: "L",
    109: "M", 110: "N", 111: "O", 112: "P", 113: "Q",
    115: "S", 116: "T", 117: "U", 118: "V", 119: "W", 120: "X",
    121: "Y", 122: "Z",
    65362: "↑", 65364: "↓", 65361: "←", 65363: "→"
}


def key_to_string(key_code: int) -> str:
    """Преобразует код клавиши в читаемую строку"""
    return ALLOWED_KEYS.get(key_code, f"[{key_code}]")


class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.hint_text = None
        self.btn_fullscreen = None
        self.background_color = WINDOW_MENU_COLOR
        self.UIman = arcade.gui.UIManager()
        self.title_text = None

        self.waiting_for_key = False
        self.current_binding = None
        self.key_buttons = {}

        self.settings_path = pathlib.Path(__file__).parent / "settings.json"
        self.settings = self.load_settings()

        self.setup()

    def load_settings(self) -> dict:
        """Загружает настройки из JSON"""
        try:
            if self.settings_path.exists():
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")

        return {
            "Fire": {"UP": 119, "LEFT": 97, "INTER": 115, "RIGHT": 100},
            "Water": {"UP": 65362, "LEFT": 65361, "INTER": 65364, "RIGHT": 65363},
            "fullscreen": False
        }

    def save_settings(self):
        """Сохраняет настройки в JSON"""
        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    def setup(self):
        self.UIman.enable()
        self.UIman.clear()

        self.title_text = arcade.Text(
            "Settings",
            self.window.width / 2,
            self.window.height - 100,
            anchor_x="center",
            **TITLE_STYLE
        )

        self.hint_text = arcade.Text(
            "",
            self.window.width / 2,
            self.window.height / 2,
            anchor_x="center",
            anchor_y="center",  # Добавили центровку по вертикали
            color=arcade.color.WHITE,
            font_size=20,  # Чуть уменьшили шрифт (было 24)
            bold=True,
            multiline=True,  # Разрешаем перенос текста!
            width=WINDOW_SIZE[0] - 60,  # Жестко ограничиваем ширину (размер маленького окна минус отступы)
            align="center"  # Выравниваем текст по центру
        )

        anchor_layout = arcade.gui.UIAnchorLayout()
        main_vbox = arcade.gui.UIBoxLayout(space_between=BUTTON_MARGIN, vertical=True)
        current_state = self.settings.get("fullscreen", False)
        btn_text = "Fullscreen: ON" if current_state else "Fullscreen: OFF"

        self.btn_fullscreen = arcade.gui.UIFlatButton(
            text=btn_text,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            style=BUTTON_STYLE
        )
        self.btn_fullscreen.on_click = self.on_click_fullscreen
        main_vbox.add(self.btn_fullscreen)

        fire_label = arcade.gui.UILabel(
            text="Fire Controls",
            font_size=16,
            font_name="georgia",
            text_color=arcade.color.DARK_RED,
            bold=True
        )
        main_vbox.add(fire_label)

        fire_hbox = arcade.gui.UIBoxLayout(space_between=8, vertical=False)
        for action in ["LEFT", "UP", "INTER", "RIGHT"]:
            btn = self.create_key_button("Fire", action)
            fire_hbox.add(btn)
        main_vbox.add(fire_hbox)

        water_label = arcade.gui.UILabel(
            text="Water Controls",
            font_size=16,
            font_name="georgia",
            text_color=arcade.color.DARK_BLUE,
            bold=True
        )
        main_vbox.add(water_label)

        water_hbox = arcade.gui.UIBoxLayout(space_between=8, vertical=False)
        for action in ["LEFT", "UP", "INTER", "RIGHT"]:
            btn = self.create_key_button("Water", action)
            water_hbox.add(btn)
        main_vbox.add(water_hbox)

        btn_reset = arcade.gui.UIFlatButton(
            text="Reset Controls",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            style=BUTTON_STYLE
        )
        btn_reset.on_click = self.on_click_reset
        main_vbox.add(btn_reset)

        btn_back = arcade.gui.UIFlatButton(
            text="Back",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            style=BUTTON_STYLE
        )
        btn_back.on_click = self.on_click_back
        main_vbox.add(btn_back)

        anchor_layout.add(child=main_vbox, anchor_x="center_x", anchor_y="center_y", align_y=-20)
        self.UIman.add(anchor_layout)

    def create_key_button(self, player: str, action: str) -> arcade.gui.UIFlatButton:
        """Создаёт кнопку для переназначения клавиши"""
        key_str = key_to_string(self.settings[player][action])

        action_icons = {"LEFT": "◀", "UP": "▲", "RIGHT": "▶", "INTER": "▼"}
        icon = action_icons.get(action, "?")

        btn = arcade.gui.UIFlatButton(
            text=f"{icon}\n{key_str}",
            width=CONTROL_BUTTON_WIDTH,
            height=CONTROL_BUTTON_HEIGHT,
            style=BUTTON_STYLE
        )

        self.key_buttons[(player, action)] = btn
        btn.on_click = lambda event, p=player, a=action: self.start_key_binding(p, a)

        return btn

    def start_key_binding(self, player: str, action: str):
        """Процесс переназначения клавиши"""
        self.waiting_for_key = True
        self.current_binding = (player, action)
        action_names = {"LEFT": "Left", "UP": "Up", "RIGHT": "Right", "INTER": "Down"}
        self.hint_text.text = f"Press new key for {player} {action_names.get(action, action)}...\n(ESC to cancel)"
        self.UIman.disable()

    def on_key_press(self, symbol: int, modifiers: int):
        """Обработка нажатия клавиши"""
        if self.waiting_for_key:
            if symbol not in ALLOWED_KEYS:
                self.finish_binding()
                return

            player, action = self.current_binding
            conflict = self.check_key_conflict(symbol, player, action)
            if conflict:
                self.finish_binding()
                return
            self.settings[player][action] = symbol
            self.save_settings()

            self.update_button_text(player, action)
            self.finish_binding()

        elif symbol == arcade.key.ESCAPE:
            self.on_click_back(None)

    def check_key_conflict(self, key_code: int, current_player: str, current_action: str) -> bool:
        """Проверка на использование клавиши."""
        for player in ["Fire", "Water"]:
            for action, code in self.settings[player].items():
                if code == key_code:
                    if player == current_player and action == current_action:
                        continue
                    return True
        return False

    def finish_binding(self):
        """Завершает режим ожидания клавиши от человека"""
        self.waiting_for_key = False
        self.current_binding = None
        self.hint_text.text = ""
        self.UIman.enable()

    def update_button_text(self, player: str, action: str):
        """Обновляет текст на кнопке у управления"""
        btn = self.key_buttons.get((player, action))
        if btn:
            key_code = self.settings[player][action]
            action_icons = {"LEFT": "◀", "UP": "▲", "RIGHT": "▶", "INTER": "▼"}
            icon = action_icons.get(action, "?")
            btn.text = f"{icon}\n{key_to_string(key_code)}"

    def on_click_reset(self, event):
        """Сбрасывает управление"""
        self.settings["Fire"] = {"UP": 119, "LEFT": 97, "INTER": 115, "RIGHT": 100}
        self.settings["Water"] = {"UP": 65362, "LEFT": 65361, "INTER": 65364, "RIGHT": 65363}
        self.save_settings()
        for (player, action) in self.key_buttons.keys():
            self.update_button_text(player, action)

    def on_click_fullscreen(self, event):
        self.window.set_fullscreen(not self.window.fullscreen)
        self.settings["fullscreen"] = self.window.fullscreen

        if self.window.fullscreen:
            self.btn_fullscreen.text = "Fullscreen: ON"
        else:
            self.btn_fullscreen.text = "Fullscreen: OFF"
            self.window.set_size(int(WINDOW_SIZE[0]), int(WINDOW_SIZE[1]))

        self.title_text.x = self.window.width / 2
        self.title_text.y = self.window.height - 100

        self.hint_text.x = self.window.width / 2
        self.hint_text.y = self.window.height / 2
        self.save_settings()

    def on_click_back(self, event):
        from src.menu_view import MenuView
        view = MenuView()
        self.window.show_view(view)

    def on_show_view(self):
        self.UIman.enable()
        self.waiting_for_key = False
        self.current_binding = None
        self.hint_text.text = ""

    def on_hide_view(self):
        self.UIman.disable()

    def on_draw(self):
        self.clear()
        if self.waiting_for_key:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(self.window.width / 2, self.window.height / 2,
                                 self.window.width, self.window.height),
                (0, 0, 0, 200)
            )
            self.hint_text.draw()
        else:
            self.UIman.draw()
            if self.title_text:
                self.title_text.draw()
