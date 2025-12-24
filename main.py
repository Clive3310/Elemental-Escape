import arcade
from src import menu_view


def main():
    window = arcade.Window(title="Elemental Escape")
    window.show_view(menu_view.MenuView())
    arcade.run()


if __name__ == "__main__":
    main()
