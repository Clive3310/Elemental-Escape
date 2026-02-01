import pathlib

import arcade.hitbox

from src.constants import *


class Player(arcade.Sprite):
    def __init__(self, position, is_fire: bool = True):
        super().__init__()
        self.position = position
        self.is_fire = is_fire
        self.scale = PLAYER_SCALING
        self.setup()

    def setup(self):
        base_path = pathlib.Path(__file__).absolute().parent.parent.parent / "assets" / "imgs"
        if self.is_fire:
            path_0 = base_path / "Fireboy-0.png"
            path_1 = base_path / "Fireboy-1.png"
            path_2 = base_path / "Fireboy-2.png"
        else:
            path_0 = base_path / "Watergirl-0.png"
            path_1 = base_path / "Watergirl-1.png"
            path_2 = base_path / "Watergirl-2.png"
        self.textures = [arcade.load_texture(path_0), arcade.load_texture(path_1), arcade.load_texture(path_2)]
        self.texture = self.textures[0]
        self.t_id = 0

        self.moving = False
        self.on_ground = True

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        super().update(delta_time)
        if not self.moving:
            self.change_x = int(self.change_x * FRICTION) if self.change_x * FRICTION > 0 else 0
        if self.change_y != 0:
            self.on_ground = False
        else:
            self.on_ground = True

        if self.change_x > 0:
            if self.t_id != 1:
                self.texture = self.textures[1]
                self.t_id = 1
        elif self.change_x < 0:
            if self.t_id != 2:
                self.texture = self.textures[2]
                self.t_id = 2
        else:
            if self.t_id != 0:
                self.texture = self.textures[0]
                self.t_id = 0
