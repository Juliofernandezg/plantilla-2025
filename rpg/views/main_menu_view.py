# """
# Main Menu
# """
import arcade
import arcade.gui

from rpg.configuracion_global import ConfiguracionGlobal


class MainMenuView(arcade.View):
    """
    This class acts as the game view for the main menu screen and its buttons. Accessed by hitting ESC. That logic can be referenced in game_view.py
    """

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

        # --- Required for all code that uses UI element, a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        resume_button = arcade.gui.UIFlatButton(text="Volver al juego", width=350, style=button_style)
        self.v_box.add(resume_button.with_space_around(bottom=40))
        resume_button.on_click = self.on_click_resume

        settings_button = arcade.gui.UIFlatButton(text="Opciones", width=350, style=button_style)
        self.v_box.add(settings_button.with_space_around(bottom=40))
        settings_button.on_click = self.on_click_settings

        controls_button = arcade.gui.UIFlatButton(text="Controles", width=350, style=button_style)
        self.v_box.add(controls_button.with_space_around(bottom=40))
        controls_button.on_click = self.on_click_controls

        new_game_button = arcade.gui.UIFlatButton(text="Nueva partida", width=350, style=button_style)
        self.v_box.add(new_game_button.with_space_around(bottom=40))
        new_game_button.on_click = self.on_click_new_game

        quit_button = arcade.gui.UIFlatButton(text="Cerrar juego", width=350, style=button_style)
        self.v_box.add(quit_button.with_space_around(bottom=40))
        quit_button.on_click = self.on_click_quit
        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        """
        Method that redraws the UI buttons each time we call the pause menu. See game_view.py for more.
        input: None
        output: None
        """
        self.clear()
        self.manager.draw()

        valor_brillo = 255 - int((ConfiguracionGlobal.brillo / 100) * 255)
        arcade.draw_lrtb_rectangle_filled(
            0, self.window.width, self.window.height, 0,
            (valor_brillo, valor_brillo, valor_brillo, 50)
        )

    # call back methods for buttons:
    def on_click_resume(self, event):
        print("show game view")
        self.window.show_view(self.window.views["game"])

    def on_click_settings(self, event):
        print("show settings view")
        self.window.show_view(self.window.views["settings"])

    def on_click_controls(self, event):
            print("show controls view")
            self.window.show_view(self.window.views["controls"])

    def on_click_new_game(self, event):
        print("restart game")
        self.window.views["game"].setup()
        self.window.show_view(self.window.views["game"])

    def on_click_quit(self, event):
        print("quitting")
        self.window.close()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            print("show game view")
            self.window.show_view(self.window.views["game"])
