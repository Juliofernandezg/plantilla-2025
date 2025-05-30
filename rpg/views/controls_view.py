import arcade
import arcade.gui

from rpg.configuracion_global import ConfiguracionGlobal
from rpg.views.main_controls_view import ControlsUI


class ControlsView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.controls_ui = None

    def setup(self):
        pass

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

        # Crear la UI de controles y asignar callback al botón
        self.controls_ui = ControlsUI(self.manager)

    def on_draw(self):
        self.clear()
        self.manager.draw()

        valor_brillo = 255 - int((ConfiguracionGlobal.brillo / 100) * 255)
        arcade.draw_lrtb_rectangle_filled(
            0, self.window.width, self.window.height, 0,
            (valor_brillo, valor_brillo, valor_brillo, 50)
        )

        arcade.draw_text(
            "Controles",
            self.window.width / 2,
            self.window.height - 80,
            arcade.color.ALLOY_ORANGE,
            48,
            anchor_x="center",
        )

    def on_hide_view(self):
        self.manager.disable()
        self.controls_ui.destroy()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["main_menu"])