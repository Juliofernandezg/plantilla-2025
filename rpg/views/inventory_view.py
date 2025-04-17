"""
Inventory
"""
import arcade
from arcade.color import BLACK, WHITE


class InventoryView(arcade.View):
    def __init__(self):
        super().__init__()
        self.started = False
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        inv_left = 50
        inv_right = (self.window.width / 2) + 100
        capacity = 3
        gap_hotbar = 25
        gab_inventories = 50
        field_width = (inv_right - 50 - (gap_hotbar * (capacity - 1))) / (capacity)
        center_x_sprite = (self.window.width - ((self.window.width / 2) +100 ))/ 2 + ((self.window.width / 2) +100 )
        center_y_sprite = self.window.height/2
        arcade.start_render()
        arcade.draw_text(
            "Inventory",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        arcade.draw_lrtb_rectangle_filled(inv_left, inv_right, (self.window.height - 100), 175, WHITE)
        arcade.draw_lrtb_rectangle_outline(inv_left, inv_right, (self.window.height - 100), 175, BLACK, 3)

        for i in range (capacity):
            start = 50 + i * (field_width + 25)
            if i < 1:
                arcade.draw_lrtb_rectangle_filled(50, 50 + field_width, 150, 50, WHITE)
                arcade.draw_lrtb_rectangle_outline(50, 50 + field_width, 150, 50, BLACK, 3)
            else:
                arcade.draw_lrtb_rectangle_filled(start, start + field_width, 150, 50 , WHITE)
                arcade.draw_lrtb_rectangle_outline(start, start + field_width, 150, 50 , BLACK, 3)

        arcade.draw_lrtb_rectangle_filled(inv_right + gab_inventories, self.window.width - 50, (self.window.height - 100), 50, WHITE)
        arcade.draw_lrtb_rectangle_outline(inv_right + gab_inventories, self.window.width - 50, (self.window.height - 100), 50, BLACK, 3)
        texture = arcade.load_texture(":characters:Boss/prueba.png")
        arcade.draw_scaled_texture_rectangle(center_x_sprite, center_y_sprite, texture, 3.5)
    def setup(self):
        pass
    def on_show_view(self):
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)


    def on_key_press(self, symbol: int, modifiers: int):
        close_inputs = [
            arcade.key.ESCAPE,
            arcade.key.I
        ]
        if symbol in close_inputs:
            self.window.show_view(self.window.views["game"])
