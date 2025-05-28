"""
Settings
"""
import arcade
import rpg.constants as constants


class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.volume = 50  # 0 a 100
        self.brightness = 50  # 0 a 100
        self.bar_width = 200
        self.bar_height = 30
        self.volume_bar_pos = (100, 400)
        self.brightness_bar_pos = (100, 300)

    def setup(self):
        # Método reintegrado para compatibilidad con otras vistas
        # Puedes usarlo para reiniciar valores si es necesario
        self.volume = 50
        self.brightness = 50

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Settings", self.window.width / 2, self.window.height - 50,
                         arcade.color.ALLOY_ORANGE, 44, anchor_x="center")

        # Dibujar barras
        self.draw_bar(self.volume_bar_pos, self.volume, "Volumen")
        self.draw_bar(self.brightness_bar_pos, self.brightness, "Brillo")

        # Simular brillo con overlay
        brightness_overlay = 255 - int((self.brightness / 100) * 255)
        arcade.draw_lrtb_rectangle_filled(0, self.window.width, self.window.height, 0,
                                          (brightness_overlay, brightness_overlay, brightness_overlay, 80))

    def draw_bar(self, position, value, label):
        x, y = position
        arcade.draw_rectangle_filled(x + self.bar_width / 2, y + self.bar_height / 2,
                                     self.bar_width, self.bar_height, arcade.color.LIGHT_GRAY)
        fill_width = (value / 100) * self.bar_width
        arcade.draw_rectangle_filled(x + fill_width / 2, y + self.bar_height / 2,
                                     fill_width, self.bar_height, arcade.color.DARK_BLUE)
        arcade.draw_text(f"{label}: {value}%", x, y + 40, arcade.color.BLACK, 16)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_inside_bar(x, y, self.volume_bar_pos):
            self.volume = self.calculate_value_from_click(x, self.volume_bar_pos)
            arcade.set_sound_volume(self.volume / 100)
        elif self.is_inside_bar(x, y, self.brightness_bar_pos):
            self.brightness = self.calculate_value_from_click(x, self.brightness_bar_pos)

    def is_inside_bar(self, x, y, position):
        bx, by = position
        return bx <= x <= bx + self.bar_width and by <= y <= by + self.bar_height

    def calculate_value_from_click(self, x, position):
        bx, _ = position
        relative_x = max(0, min(x - bx, self.bar_width))
        return int((relative_x / self.bar_width) * 100)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["main_menu"])
