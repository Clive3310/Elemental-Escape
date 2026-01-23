import arcade
import arcade.gui

DEV = False
WINDOW_MENU_COLOR = arcade.color.BRONZE_YELLOW
WINDOW_SIZE = (516, 716)
font_size_button = int(WINDOW_SIZE[0] // 27.77)
font_name_button = "georgia"
BUTTON_STYLE = {
    'normal': arcade.gui.UIFlatButton.UIStyle(
        font_size=font_size_button,
        font_name=(font_name_button,),
        font_color=arcade.color.BLACK,
        bg=arcade.color.WHEAT,
        border=arcade.color.GOLD,
        border_width=10,
    ),
    'hover': arcade.gui.UIFlatButton.UIStyle(
        font_size=font_size_button,
        font_name=(font_name_button,),
        font_color=arcade.color.BLACK,
        bg=arcade.color.YELLOW_ROSE,
        border=arcade.color.YELLOW_GREEN,
        border_width=10,
    ),
    'press': arcade.gui.UIFlatButton.UIStyle(
        font_size=font_size_button,
        font_name=(font_name_button,),
        font_color=arcade.color.BLACK,
        bg=arcade.color.YELLOW_ROSE,
        border=arcade.color.YELLOW_GREEN,
        border_width=3,
    )
}
TITLE_STYLE = {
    "color": arcade.color.BLACK,
    "font_size": WINDOW_SIZE[0] // 15.625,
    "font_name": ("georgia",),
    "bold": True
}
TILE_SCALING = 0.7
PLAYER_SCALING = 0.03
PLAYER_SPEED = 2
PLAYER_JUMP_POWER = 7
GRAVITY = 0.5
FRICTION = 0.8
BUTTON_SCALE = 0.05
DOOR_SCALE = 0.15
DOOR_MOVE_UP_SCALE = 1
DOOR_SPEED = 60
TIMER_FONT_SIZE = 30
EXIT_SCALING = 1
STANDARD_LEVEL_DATA = {
    "Completed": False,
    "Best_time": 10000.0,
    "Stars": 0
}
MAX_LEVEL_TIME = 100.0
BASE_LEVEL_DATA = {
    "Levels": {
        "1": {
            "Completed": False,
            "Best_time": 10000.0,
            "Stars": 0
        },
        "2": {
            "Completed": False,
            "Best_time": 10000.0,
            "Stars": 0
        },
        "3": {
            "Completed": False,
            "Best_time": 10000.0,
            "Stars": 0
        },
        "4": {
            "Completed": False,
            "Best_time": 10000.0,
            "Stars": 0
        },
        "5": {
            "Completed": False,
            "Best_time": 10000.0,
            "Stars": 0
        },
        "6": {
            "Completed": False,
            "Best_time": 10000.0,
            "Stars": 0
        }
    }
}
LEVEL_COUNT = 6
FORCE_POWER = 40
