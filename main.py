import arcade
import json
import pathlib
from src import menu_view


def main():
    window = arcade.Window(title="Elemental Escape")

    settings_path = pathlib.Path(__file__).parent / "src" / "settings.json"

    try:
        if settings_path.exists():
            with open(settings_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("fullscreen") is True:
                    window.set_fullscreen(True)
    except Exception as e:
        print(f"Не удалось загрузить настройки: {e}")

    window.show_view(menu_view.MenuView())
    arcade.run()


if __name__ == "__main__":
    main()