import pathlib

from src.constants import *


class Door(arcade.Sprite):
    def __init__(self, position, color_id: int, rev: bool = False):  # 0 - yellow, 1 - red, base - yellow
        super().__init__()
        self.position = position
        self.scale = DOOR_SCALE
        self.color_id = color_id
        self.rev = rev

        self.setup()

    def setup(self):
        self.activated = False
        base_path = pathlib.Path(__file__).absolute().parent.parent.parent / "assets" / "imgs"
        match self.color_id:
            case 0:
                self.texture = arcade.load_texture(base_path / "door-yellow.png")
            case 1:
                self.texture = arcade.load_texture(base_path / "door-red.png")
            case _:
                self.texture = arcade.load_texture(base_path / "door-yellow.png")

        if self.rev:
            self.max_down = self.bottom - DOOR_MOVE_UP_SCALE * self.height
            self.least_up = self.top
        else:
            self.max_up = self.top + DOOR_MOVE_UP_SCALE * self.height
            self.least_down = self.bottom

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        super().update()
        if not self.activated:
            if self.rev:
                if self.top < self.least_up:
                    self.center_y += DOOR_SPEED * delta_time
            else:
                if self.bottom > self.least_down:
                    self.center_y -= DOOR_SPEED * delta_time
        self.activated = False

    def use(self, delta_time: float = 1 / 60):
        self.activated = True
        if self.rev:
            if self.bottom > self.max_down:
                self.center_y -= DOOR_SPEED * delta_time * 2
        else:
            if self.bottom < self.max_up:
                self.center_y += DOOR_SPEED * delta_time * 2
