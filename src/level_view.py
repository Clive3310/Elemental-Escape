from src.data_save_load import *
from src.entities.player import Player
from src.entities.button import Button
from src.entities.door import Door
from src.entities.exit import Exit
from pyglet.graphics import Batch
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
        self.player_data = load_level_data(self.ind)

        layer_options = {
            "Background": {
                "use_spatial_hash": True
            },
            "Walls": {
                "use_spatial_hash": True
            },
            "Exit": {
                "use_spatial_hash": True
            },
            "Fire": {
                "use_spatial_hash": True
            },
            "Water": {
                "use_spatial_hash": True
            }
        }

        base_path = self.base_dir.parent / "assets" / "maps"
        try:
            path = base_path / f"Level-{self.ind}.json"
            self.tile_map = arcade.load_tilemap(path, scaling=TILE_SCALING,
                                                layer_options=layer_options)
        except FileNotFoundError:
            print(f"Error: {self.ind}-Level not found")
            path = base_path / f"BaseLevel.json"
            self.tile_map = arcade.load_tilemap(path, scaling=TILE_SCALING,
                                                layer_options=layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Стены - фон
        self.wallsList = self.scene.get_sprite_list("Walls")
        self.bgList = self.scene.get_sprite_list("Background")

        # Огонь + вода
        self.waterList = self.scene.get_sprite_list("Water")
        self.fireList = self.scene.get_sprite_list("Fire")

        # Двери
        self.doors_ids = dict()
        self.doors = arcade.SpriteList()
        if "DoorsData" in self.tile_map.object_lists.keys():
            for obj in self.tile_map.object_lists["DoorsData"]:
                door = Door(obj.shape, obj.properties["color"], obj.properties["reversed"])
                self.doors_ids[obj.properties["id"]] = door
                self.doors.append(door)
        self.scene.add_sprite_list("Doors", sprite_list=self.doors)

        # Кнопки
        self.buttons = arcade.SpriteList()
        if "ButtonsData" in self.tile_map.object_lists.keys():
            for obj in self.tile_map.object_lists["ButtonsData"]:
                button = Button(obj.shape, obj.properties["id"], obj.properties["color"])
                self.buttons.append(button)
        self.scene.add_sprite_list("Buttons", sprite_list=self.buttons)

        # Игроки
        self.fire_spawn_pos = self.scene.get_sprite_list("FireSpawn").pop().position
        self.water_spawn_pos = self.scene.get_sprite_list("WaterSpawn").pop().position

        self.player_fire = Player(self.fire_spawn_pos, True)
        self.player_water = Player(self.water_spawn_pos, False)
        self.players = arcade.SpriteList()
        self.players.extend((self.player_fire, self.player_water))

        self.scene.add_sprite_list("Players", sprite_list=self.players)

        self.wallsList.extend(self.doors)

        self.phisics_fire = arcade.PhysicsEnginePlatformer(self.player_fire, platforms=self.wallsList,
                                                           gravity_constant=GRAVITY, walls=self.wallsList)
        self.phisics_water = arcade.PhysicsEnginePlatformer(self.player_water, platforms=self.wallsList,
                                                            gravity_constant=GRAVITY, walls=self.wallsList)

        self.time = 0.0
        self.time_batch = Batch()

        self.deaths = 0

        # Выходы
        self.exits = arcade.SpriteList()
        self.exit_fire = None
        self.exit_water = None
        for obj in self.tile_map.object_lists["Exits"]:
            if obj.properties["fire"]:
                self.exit_fire = Exit(obj.shape, obj.properties["fire"])
            else:
                self.exit_water = Exit(obj.shape, obj.properties["fire"])
        self.exits.extend((self.exit_fire, self.exit_water))
        self.scene.add_sprite_list_before("Exits", sprite_list=self.exits, before="Players")

    def on_draw(self):
        self.clear()
        self.scene.draw()

        self.time_text = arcade.Text(f"{round(self.time, 2)}", WINDOW_SIZE[0] // 2 - TIMER_FONT_SIZE,
                                     WINDOW_SIZE[1] - TIMER_FONT_SIZE,
                                     color=arcade.color.BLACK, font_size=TIMER_FONT_SIZE, batch=self.time_batch)
        self.time_batch.draw()

    def on_update(self, delta_time: float):
        self.players.update()

        self.button_func(delta_time)
        self.doors.update()

        self.phisics_fire.update()
        self.phisics_water.update()

        deadge = self.death_check()
        if deadge:
            self.restart()

        self.time += delta_time

        self.end_check()

    def restart(self):
        self.player_fire.position = self.fire_spawn_pos
        self.player_fire.change_x, self.player_fire.change_y = 0, 0

        self.player_water.position = self.water_spawn_pos
        self.player_water.change_x, self.player_water.change_y = 0, 0

    def death_check(self):
        if self.player_fire.collides_with_list(self.waterList):
            return True

        if self.player_water.collides_with_list(self.fireList):
            return True
        return False

    def ending(self):
        save_level_data(self.ind, "Completed", True)

        new_record = False
        if round(self.time, 2) < self.player_data["Best_time"]:
            new_record = True
            save_level_data(self.ind, "Best_time", round(self.time, 2))

        star_count = 1
        star_count += 1 if self.time < MAX_LEVEL_TIME else 0
        star_count += 1 if not self.deaths else 0
        if star_count > self.player_data["Stars"]:
            save_level_data(self.ind, "Stars", star_count)

        from src.ending_view import EndingView
        view = EndingView(self.ind, round(self.time, 2), self.deaths, new_record)
        self.window.show_view(view)

    def end_check(self):
        if (self.player_fire.collides_with_sprite(self.exit_fire) and
                self.player_water.collides_with_sprite(self.exit_water)):
            self.ending()

    def button_func(self, delta_time: float):
        used = set()
        for but in self.player_fire.collides_with_list(self.buttons):
            door_id = but.aid
            try:
                self.doors_ids[door_id].use(delta_time)
                used.add(door_id)
            except KeyError:
                print(f"Error: door {door_id} wasn't found")

        for but in self.player_water.collides_with_list(self.buttons):
            door_id = but.aid
            try:
                if door_id in used:
                    continue
                self.doors_ids[door_id].use(delta_time)
            except KeyError:
                print(f"Error: door {door_id} wasn't found")

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
            _view = ChooseView()
            self.window.show_view(_view)

        if symbol == arcade.key.R:
            self.setup()

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
    view = LevelView(ind=1)
    window.show_view(view)
    arcade.run()
