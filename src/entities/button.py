from src.constants import *
import pathlib


class Button(arcade.Sprite):
    def __init__(self, position, aid: int, color_id: int):  # 0 - yellow, 1 - red, base - yellow
        super().__init__()
        self.position = position
        self.aid = aid
        self.color_id = color_id
        self.scale = BUTTON_SCALE

        self.setup()

    def setup(self):
        base_path = pathlib.Path(__file__).absolute().parent.parent.parent / "assets" / "imgs"
        match self.color_id:
            case 0:
                self.texture = arcade.load_texture(base_path / "button-yellow.png")
            case 1:
                self.texture = arcade.load_texture(base_path / "button-red.png")
            case _:
                self.texture = arcade.load_texture(base_path / "button-yellow.png")
