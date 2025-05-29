import arcade


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
        arcade.draw_text("LO HAN REVENTAO AL POBRE", self.window.width / 2,
                         self.window.height / 2 + 60,
                         arcade.color.DARK_RED, 50, anchor_x="center")
        arcade.draw_text("Pulsa cualquier tecla para volver al menú principal", self.window.width / 2,
                         (self.window.height / 2) - 40,
                         arcade.color.DARK_RED, 30, anchor_x="center")

    def on_update(self, delta_time: float):
        from rpg.views import TitleView
        self.window.views["title_view"] = TitleView()
        self.window.views["title_view"].setup()

    def on_key_press(self, symbol: int, modifiers: int):

        self.window.show_view(self.window.views["title_view"])