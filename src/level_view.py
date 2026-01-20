from src.constants import *
from src.entities.player import Player
import arcade
import json
import pathlib


class LevelView(arcade.View):
    def __init__(self, ind: int = 1):
        super().__init__()
        self.ind = ind
        if not self.window.fullscreen:
            self.window.size = WINDOW_SIZE
        self.tile_map = None
        self.scene = None
        self.background_color = arcade.color.BLACK
        self.base_dir = pathlib.Path(__file__).absolute().parent
        path = self.base_dir / "settings.json"
        with path.open() as f:
            self.rule_set = json.load(f)

        self.setup()

    def setup(self):
        layer_options = {
            "Background": {
                "use_spatial_hash": True
            },
            "Walls": {
                "use_spatial_hash": True
            },
            "Exit": {
                "use_spatial_hash": True
            }
        }

        base_path = self.base_dir.parent / "assets" / "maps"
        try:
            path = base_path / f"Level{self.ind}.json"
            self.tile_map = arcade.load_tilemap(path, scaling=TILE_SCALING,
                                                layer_options=layer_options)
        except FileNotFoundError:
            print(f"Error: {self.ind}-Level not found")
            path = base_path / f"BaseLevel.json"
            self.tile_map = arcade.load_tilemap(path, scaling=TILE_SCALING,
                                                layer_options=layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.wallsList = self.scene.get_sprite_list("Walls")
        self.bgList = self.scene.get_sprite_list("Background")

        self.fire_spawn_pos = self.scene.get_sprite_list("FireSpawn").pop().position
        self.water_spawn_pos = self.scene.get_sprite_list("WaterSpawn").pop().position

        self.player_fire = Player(self.fire_spawn_pos, True)
        self.player_water = Player(self.water_spawn_pos, False)

        self.scene.add_sprite("Fire", self.player_fire)
        self.scene.add_sprite("Water", self.player_water)

        self.phisics_fire = arcade.PhysicsEnginePlatformer(self.player_fire, platforms=self.wallsList,
                                                           gravity_constant=GRAVITY, walls=self.wallsList)
        self.phisics_water = arcade.PhysicsEnginePlatformer(self.player_water, platforms=self.wallsList,
                                                            gravity_constant=GRAVITY, walls=self.wallsList)

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def on_update(self, delta_time: float):
        self.player_fire.update()
        self.player_water.update()
        self.phisics_fire.update()
        self.phisics_water.update()

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == self.rule_set["Fire"]["LEFT"]:
            self.player_fire.change_x = -PLAYER_SPEED
            self.player_fire.moving = True
        if symbol == self.rule_set["Fire"]["RIGHT"]:
            self.player_fire.change_x = PLAYER_SPEED
            self.player_fire.moving = True

        if symbol == self.rule_set["Water"]["LEFT"]:
            self.player_water.change_x = -PLAYER_SPEED
            self.player_water.moving = True
        if symbol == self.rule_set["Water"]["RIGHT"]:
            self.player_water.change_x = PLAYER_SPEED
            self.player_water.moving = True

        if symbol == self.rule_set["Fire"]["UP"] and self.player_fire.on_ground:
            self.player_fire.change_y = PLAYER_JUMP_POWER
        if symbol == self.rule_set["Water"]["UP"] and self.player_water.on_ground:
            self.player_water.change_y = PLAYER_JUMP_POWER

        if symbol == arcade.key.ESCAPE and DEV:
            from src.lv_choose_view import ChooseView
            view = ChooseView()
            self.window.show_view(view)

    def on_key_release(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == self.rule_set["Fire"]["LEFT"]:
            self.player_fire.moving = False
        if symbol == self.rule_set["Fire"]["RIGHT"]:
            self.player_fire.moving = False

        if symbol == self.rule_set["Water"]["LEFT"]:
            self.player_water.moving = False
        if symbol == self.rule_set["Water"]["RIGHT"]:
            self.player_water.moving = False


if __name__ == "__main__":
    window = arcade.Window()
    view = LevelView()
    window.show_view(view)
    arcade.run()
