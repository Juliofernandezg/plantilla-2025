"""
Inventory
"""
import arcade
from arcade.color import BLACK, WHITE, REDWOOD, ASH_GREY

from rpg.configuracion_global import ConfiguracionGlobal
from rpg.views.game_view import GameView


class InventoryView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_sprite = GameView.player_sprite
        self.started = False
        self.selected_item = 1
        self.selected_hotbar = 0
        self.capacity_hotbar = 3
        self.capacity_inventory = 5
        self.number_sprites = []
        arcade.set_background_color(arcade.color.ALMOND)

    def load_hotbar_sprites(self):
        first_number_pad_sprite_index = 51
        last_number_pad_sprite_index = 61

        self.number_sprites = arcade.load_spritesheet(
            file_name="../resources/tilesets/input_prompts_kenney.png",
            sprite_width=16,
            sprite_height=16,
            columns=34,
            count=816,
            margin=1,
        )[first_number_pad_sprite_index:last_number_pad_sprite_index]
        
    def on_draw(self):
        colores = [WHITE, ASH_GREY]

        valor_brillo = 255 - int((ConfiguracionGlobal.brillo / 100) * 255)
        arcade.draw_lrtb_rectangle_filled(
            0, self.window.width, self.window.height, 0,
            (valor_brillo, valor_brillo, valor_brillo, 50)
        )

        inv_left = 50
        inv_right = (self.window.width / 2) + 100
        ancho = inv_right - inv_left
        gap_hotbar = 25
        gab_inventories = 50
        field_width = (inv_right - 50 - (gap_hotbar * (self.capacity_hotbar - 1))) / self.capacity_hotbar
        field_height = (self.window.height - 100 - 175) / self.capacity_inventory
        center_x_sprite = (self.window.width - ((self.window.width / 2) +100 ))/ 2 + ((self.window.width / 2) +100 )
        center_y_sprite = self.window.height/2
        arcade.start_render()
        arcade.draw_text(
            "Inventario",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        # Interfaz Inventario
        for i in range(self.capacity_inventory):
            y1 = (self.window.height -100) - (i * field_height)
            y2 = y1 - field_height
            color = colores[i%2]
            arcade.draw_lrtb_rectangle_filled(inv_left, inv_right, y1, y2, color)
            hotkey_sprite = self.number_sprites[i+self.capacity_hotbar]
            hotkey_sprite.draw_scaled(inv_left + 30, y1 - 30, 2)
            if len(GameView.player_sprite.Inventory) == i+1 :
                item_name = GameView.player_sprite.Inventory[i]["short_name"]
            else:
                item_name = ""
            text = f"     {item_name}"
            arcade.draw_text(text, inv_left +10, (y1-y2)/ 2, arcade.color.ALLOY_ORANGE, 16)


        arcade.draw_lrtb_rectangle_outline(inv_left, inv_right, (self.window.height - 100), 175, BLACK, 3)

        for i in range(self.capacity_inventory):
            y1 = (self.window.height -100) - (i * field_height)
            y2 = y1 - field_height
            if i + self.capacity_hotbar == self.selected_item - 1:
                arcade.draw_lrtb_rectangle_outline(
                    inv_left , inv_right, y1 , y2 , REDWOOD, 3
                )
        # Interfaz Hotbar
        for i in range (self.capacity_hotbar):
            start = 50 + i * (field_width + 25)
            hotkey_sprite = self.number_sprites[i]
            if i < 1:
                arcade.draw_lrtb_rectangle_filled(50, 50 + field_width, 150, 50, WHITE)
                arcade.draw_lrtb_rectangle_outline(50, 50 + field_width, 150, 50, BLACK, 3)
                hotkey_sprite.draw_scaled(75, 125, 2)
                if self.selected_item == 1:
                    arcade.draw_lrtb_rectangle_outline(50, 50 + field_width, 150, 50, REDWOOD, 3)

            else:
                arcade.draw_lrtb_rectangle_filled(start, start + field_width, 150, 50 , WHITE)
                arcade.draw_lrtb_rectangle_outline(start, start + field_width, 150, 50 , BLACK, 3)
                hotkey_sprite.draw_scaled(start + 25, 125, 2)
                if self.selected_item-1 == i :
                    x1 = 50 + ((field_width + gap_hotbar) * i)
                    x2 = x1 + field_width
                    arcade.draw_lrtb_rectangle_outline(x1, x2, 150, 50, REDWOOD, 3)

            if len(GameView.player_sprite.hotbar) > i and i < 1:
                item_name = GameView.player_sprite.hotbar[i]["short_name"]
                y_text = 50 + (150 - 50)/2
                x_text = 55
            elif len(GameView.player_sprite.hotbar) > i >= 1:
                item_name = GameView.player_sprite.hotbar[i]["short_name"]
                y_text = 50 + (150-50)/2
                x_text = start
            else:
                y_text = 50 + (150 - 50) / 2
                x_text = start
                item_name = ""
            text = f"     {item_name}"
            arcade.draw_text(text, x_text, y_text, arcade.color.ALLOY_ORANGE, 16)
        # Interfaz Personaje(WIP)
        texture = arcade.load_texture(":characters:linkillo_picture.png")
        arcade.draw_scaled_texture_rectangle(center_x_sprite, center_y_sprite, texture, 0.35)

    def setup(self):
        self.load_hotbar_sprites()
    def on_show_view(self):
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    def interact(self):

        if self.selected_item <= 3 and self.player_sprite.hotbar[self.selected_item - 1]["heal_amount"]:
            if not len(self.player_sprite.hotbar) == 0:
                heal = self.player_sprite.hotbar[self.selected_item - 1]["heal_amount"]
                self.player_sprite.hotbar.pop(self.selected_item - 1)
                GameView.apply_heal(self, heal)
        elif self.selected_item > 3 and self.player_sprite.Inventory[self.selected_item - 1 - self.capacity_hotbar]["heal_amount"]:
            if not len(self.player_sprite.Inventory) == 0:
                heal = self.player_sprite.Inventory[self.selected_item -self.capacity_hotbar-1]["heal_amount"]
                self.player_sprite.Inventory.pop(self.selected_item -self.capacity_hotbar - 1)
                GameView.apply_heal(self, heal)


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.KEY_1:
            self.selected_item = 1
        elif symbol == arcade.key.KEY_2:
            self.selected_item = 2
        elif symbol == arcade.key.KEY_3:
            self.selected_item = 3
        elif symbol == arcade.key.KEY_4:
            self.selected_item = 4
        elif symbol == arcade.key.KEY_5:
            self.selected_item = 5

        elif symbol == arcade.key.KEY_6:
            self.selected_item = 6
        elif symbol == arcade.key.KEY_7:
            self.selected_item = 7
        elif symbol == arcade.key.KEY_8:
            self.selected_item = 8

        elif symbol == arcade.key.SPACE:
            self.interact()

        close_inputs = [
            arcade.key.ESCAPE,
            arcade.key.I
        ]
        if symbol in close_inputs:
            self.window.show_view(self.window.views["game"])
