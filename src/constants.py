import arcade.gui

WINDOW_BASE_COLOR = arcade.color.BRONZE_YELLOW
WINDOW_SIZE = (1000, 700)
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
