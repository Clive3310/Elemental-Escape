from src.constants import *


class Player(arcade.Sprite):
    def __init__(self, position, is_fire: bool = True):
        super().__init__()
        self.position = position
        self.is_fire = is_fire
        self.scale = PLAYER_SCALING
        self.setup()

    def setup(self):
        base_path = "/".join(__file__.split("\\")[:-3] + ['assets', 'imgs'])
        if self.is_fire:
            path = base_path + "/Fireboy-0.png"
        else:
            path = base_path + "/Watergirl-0.png"
        self.texture = arcade.load_texture(path)

        self.moving = False
        self.on_ground = True

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        super().update()
        if not self.moving:
            self.change_x *= FRICTION
        if self.change_y != 0:
            self.on_ground = False
        else:
            self.on_ground = True
