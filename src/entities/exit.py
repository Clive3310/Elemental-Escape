import pathlib

from src.constants import *


class Exit(arcade.Sprite):
    def __init__(self, position, is_fire_exit: bool = True):
        super().__init__()
        self.position = position
        self.is_fire_exit = is_fire_exit
        self.scale = EXIT_SCALING
        self.setup()

    def setup(self):
        base_path = pathlib.Path(__file__).absolute().parent.parent.parent / "assets" / "imgs"
        if self.is_fire_exit:
            path = base_path / "exit_fire.png"
        else:
            path = base_path / "exit_water.png"
        self.texture = arcade.load_texture(path)
