"""
First game menu
"""
import arcade
import arcade.gui

from rpg.views.loading_view import LoadingView
from rpg.views.main_settings_view import MainSettingsView


class TitleView(arcade.View):
    def __init__(self):
        super().__init__()

        button_style = {
            "font_name": ("Arial",),
            "font_size": 18,
            "font_color": arcade.color.WHITE,
            "bg_color": arcade.color.ALLOY_ORANGE,
            "border_color": arcade.color.ALMOND,
            "border_width": 4,
        }

        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()


        play_button = arcade.gui.UIFlatButton(text="PLAY", width=350, style=button_style)
        self.v_box.add(play_button.with_space_around(bottom=40))
        play_button.on_click = self.on_click_play


        settings_button = arcade.gui.UIFlatButton(text="SETTINGS", width=350, style=button_style)
        self.v_box.add(settings_button.with_space_around(bottom=40))
        settings_button.on_click = self.on_click_settings


        controls_button = arcade.gui.UIFlatButton(text="CONTROLS", width=350, style=button_style)
        self.v_box.add(controls_button.with_space_around(bottom=40))
        controls_button.on_click = self.on_click_controls


        quit_button = arcade.gui.UIFlatButton(text="QUIT", width=350, style=button_style)
        self.v_box.add(quit_button.with_space_around(bottom=40))
        quit_button.on_click = self.on_click_quit


        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-100,  # set v.box 100 pixels down
                child=self.v_box
            )
        )


    def on_draw(self):
        self.clear()
        self.manager.draw()

        arcade.draw_text(
            "GAME_TITLE",
            self.window.width / 2,
            self.window.height / 1.2,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_hide_view(self):
        self.manager.disable()

    def setup(self):
        pass

    def on_update(self, delta_time: float):
        self.window.views["game_title"] = TitleView()
        self.window.views["game_title"].setup()
        self.window.views["loading"] = LoadingView()
        self.window.views["loading"].setup()
        self.window.views["main_settings"] = MainSettingsView()
        self.window.views["main_settings"].setup()
        self.window.views["controls"] = MainSettingsView() # Falta crear la vista Controls
        self.window.views["controls"].setup()

    # call back methods for buttons:
    def on_click_play(self, event):
        print("show loading view")
        self.window.show_view(self.window.views["loading"])

    def on_click_settings(self, event):
        print("show settings view")
        self.window.show_view(self.window.views["main_settings"])

    def on_click_controls(self, event):
        print("controls screen")
        self.window.views["controls"].setup()
        self.window.show_view(self.window.views["main_settings"])

    def on_click_quit(self, event):
        print("quitting")
        self.window.close()
