import arcade.color
from pyglet.graphics import Batch

from src.data_save_load import *

RECT_WIDTH = WINDOW_SIZE[0] // 1.4
RECT_HEIGHT = WINDOW_SIZE[1] // 2
BUTTON_WIDTH = WINDOW_SIZE[0] // 3.4
BUTTON_HEIGHT = WINDOW_SIZE[1] // 8
BUTTON_MARGIN = BUTTON_WIDTH // 4


class EndingView(arcade.View):
    def __init__(self, level_id: int, p_time: float, deaths: int, new_record: bool):
        super().__init__()
        self.level_id = level_id
        self.p_time = p_time
        self.deaths = deaths
        self.new_record = new_record
        if not self.window.fullscreen:
            self.window.size = WINDOW_SIZE
        self.background_color = WINDOW_MENU_COLOR
        self.ui_manager = arcade.gui.UIManager()

        self.player_data = None
        self.batch = Batch()
        self.setup()

    def setup(self):
        self.player_data = load_level_data(self.level_id)
        if self.player_data is None:
            self.player_data = STANDARD_LEVEL_DATA
        best = self.player_data['Best_time']

        # Time
        new_text_style = {
            "color": arcade.color.BLACK,
            "font_size": 11,
            "font_name": ("georgia",),
            "bold": True
        }
        if self.new_record:
            self.time_text = arcade.Text(f"New Record: {self.p_time}!", WINDOW_SIZE[0] // 2,
                                         WINDOW_SIZE[1] // 2 + RECT_HEIGHT // 2 - new_text_style['font_size'] * 2,
                                         anchor_x="center", **new_text_style, batch=self.batch)
        else:
            self.time_text = arcade.Text(f"Your time: {self.p_time} - Your best time: {best}", WINDOW_SIZE[0] // 2,
                                         WINDOW_SIZE[1] // 2 + RECT_HEIGHT // 2 - new_text_style['font_size'] * 2,
                                         anchor_x="center", **new_text_style, batch=self.batch)

        # Stars
        text = ("★ " * self.player_data["Stars"] + "☆ " * (3 - self.player_data["Stars"])).strip()
        new_text_style['font_size'] = 70
        self.star_text = arcade.Text(text, WINDOW_SIZE[0] // 2,
                                     WINDOW_SIZE[1] // 2 + new_text_style['font_size'] // 1.3,
                                     anchor_x="center",
                                     **new_text_style, batch=self.batch)

        # Deaths
        self.deaths_text = arcade.Text(str(self.deaths), WINDOW_SIZE[0] // 2,
                                       WINDOW_SIZE[1] // 3 - new_text_style["font_size"] * 0.5, anchor_x="center",
                                       **new_text_style, batch=self.batch)

        # Make ui
        self.ui_manager.enable()
        self.ui_manager.clear()

        anchor_layout = arcade.gui.UIAnchorLayout()
        v_box = arcade.gui.UIBoxLayout(space_between=BUTTON_MARGIN)
        v_box.vertical = False

        new_button_style = {
            'normal': arcade.gui.UIFlatButton.UIStyle(
                font_size=14,
                font_name=(font_name_button,),
                font_color=arcade.color.BLACK,
                bg=arcade.color.WHEAT,
                border=arcade.color.GOLD,
                border_width=10,
            ),
            'hover': arcade.gui.UIFlatButton.UIStyle(
                font_size=14,
                font_name=(font_name_button,),
                font_color=arcade.color.BLACK,
                bg=arcade.color.YELLOW_ROSE,
                border=arcade.color.YELLOW_GREEN,
                border_width=10,
            ),
            'press': arcade.gui.UIFlatButton.UIStyle(
                font_size=14,
                font_name=(font_name_button,),
                font_color=arcade.color.BLACK,
                bg=arcade.color.YELLOW_ROSE,
                border=arcade.color.YELLOW_GREEN,
                border_width=3,
            )
        }

        back_button = arcade.gui.UIFlatButton(text="Back to menu", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                              style=new_button_style)
        back_button.on_click = self.go_back
        v_box.add(back_button)

        if self.level_id + 1 < LEVEL_COUNT:
            next_button = arcade.gui.UIFlatButton(text="Next level", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                                  style=new_button_style)
            next_button.on_click = self.next_level
            v_box.add(next_button)

        anchor_layout.add(child=v_box, anchor_x="center_x", anchor_y="center_y", align_y=-30)
        self.ui_manager.add(anchor_layout)

    def go_back(self, _a):
        from src.lv_choose_view import ChooseView
        view = ChooseView()
        self.window.show_view(view)

    def next_level(self, _a):
        from src.level_view import LevelView
        view = LevelView(self.level_id + 1)
        self.window.show_view(view)

    def on_draw(self):
        self.clear()

        arcade.draw_rect_filled(arcade.rect.XYWH(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2, RECT_WIDTH, RECT_HEIGHT),
                                arcade.color.GOLD)
        self.batch.draw()
        self.ui_manager.draw()


if __name__ == "__main__":
    window = arcade.Window()
    view = EndingView(1, 0.0, 0, False)
    window.show_view(view)
    arcade.run()
