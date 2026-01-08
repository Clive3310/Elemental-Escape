import arcade

from src.constants import *


class LevelView(arcade.View):
    def __init__(self, ind: int = 1):
        super().__init__()
        self.ind = ind
        self.window.size = WINDOW_SIZE

        self.tile_map = None
        self.scene = None
        self.background_color = arcade.color.BLACK

        self.setup()

    def setup(self):
        layer_options = {
            "Background": {
                "use_spatial_hash": True
            },
            "Walls": {
                "use_spatial_hash": True
            }
        }

        base_path = "/".join(__file__.split("\\")[:-2] + ['assets', 'maps'])
        try:
            path = base_path + f"/Level{self.ind}.json"
            self.tile_map = arcade.load_tilemap(path, scaling=TILE_SCALING,
                                                layer_options=layer_options)
        except FileNotFoundError:
            print(f"Error: {self.ind}-Level not found")
            path = base_path + f"/BaseLevel.json"
            self.tile_map = arcade.load_tilemap(path, scaling=TILE_SCALING,
                                                layer_options=layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.wallsList = self.scene.get_sprite_list("Walls")
        self.bgList = self.scene.get_sprite_list("Background")

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def on_update(self, delta_time: float):
        pass

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.ESCAPE and DEV:
            from src.lv_choose_view import ChooseView
            view = ChooseView()
            self.window.show_view(view)


if __name__ == "__main__":
    window = arcade.Window()
    view = LevelView()
    window.show_view(view)
    arcade.run()
