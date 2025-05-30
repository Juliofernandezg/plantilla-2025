import arcade

from rpg.configuracion_global import ConfiguracionGlobal


class GameOver(arcade.View):
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.LIGHT_GRAY)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        arcade.start_render()

        valor_brillo = 255 - int((ConfiguracionGlobal.brillo / 100) * 255)
        arcade.draw_lrtb_rectangle_filled(
            0, self.window.width, self.window.height, 0,
            (valor_brillo, valor_brillo, valor_brillo, 50)
        )

        arcade.draw_text("LO HAN REVENTAO AL POBRE", self.window.width / 2,
                         self.window.height / 2 + 60,
                         arcade.color.DARK_RED, 50, anchor_x="center")
        arcade.draw_text("Pulsa cualquier tecla para volver a empezar", self.window.width / 2,
                         (self.window.height / 2) - 40,
                         arcade.color.DARK_RED, 30, anchor_x="center")

    def on_update(self, delta_time: float):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        print("restart game")
        self.window.views["game"].setup()
        self.window.show_view(self.window.views["game"])