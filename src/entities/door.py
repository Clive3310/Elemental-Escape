from src.constants import *
import pathlib


class Door(arcade.Sprite):
    def __init__(self, position, color_id: int):  # 0 - yellow, 1 - red, base - yellow
        super().__init__()
        self.position = position
        self.scale = DOOR_SCALE
        self.color_id = color_id

        self.setup()

    def setup(self):
        base_path = pathlib.Path(__file__).absolute().parent.parent.parent / "assets" / "imgs"
        match self.color_id:
            case 0:
                self.texture = arcade.load_texture(base_path / "door-yellow.png")
            case 1:
                self.texture = arcade.load_texture(base_path / "door-red.png")
            case _:
                self.texture = arcade.load_texture(base_path / "door-yellow.png")

        self.max_up = self.top + DOOR_MOVE_UP_SCALE * self.height
        self.leat_down = self.bottom

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        super().update()
        if self.bottom > self.leat_down:
            self.center_y -= DOOR_SPEED * delta_time

    def use(self, delta_time: float = 1 / 60):
        if self.top < self.max_up:
            self.center_y += DOOR_SPEED * delta_time * 2
