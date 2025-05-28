"""
Inventory
"""
import arcade
from arcade.color import BLACK, WHITE, REDWOOD, ASH_GREY

from rpg.views.game_view import GameView


class InventoryView(arcade.View):
    def __init__(self):
        super().__init__()
        self.started = False
        self.selected_item = 1
        self.selected_hotbar = 0
        self.number_sprites = []
        self.potions_sprites = []
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
        self.potions_sprites = arcade.load_spritesheet(
            file_name="../resources/tilesets/input_prompts_kenney.png",
            sprite_width=16,
            sprite_height=16,
            columns=34,
            count=816,
            margin=1,)[85:87]
        
    def on_draw(self):
        colores = [WHITE, ASH_GREY]
        inv_left = 50
        inv_right = (self.window.width / 2) + 100
        ancho = inv_right - inv_left
        capacity_hotbar = 3
        capacity_inventory = 5
        gap_hotbar = 25
        gab_inventories = 50
        field_width = (inv_right - 50 - (gap_hotbar * (capacity_hotbar - 1))) / capacity_hotbar
        field_height = (self.window.height - 100 - 175) / capacity_inventory
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
        # Interfaz Inventario
        for i in range(capacity_inventory):
            y1 = (self.window.height -100) - (i * field_height)
            y2 = y1 - field_height
            color = colores[i%2]
            arcade.draw_lrtb_rectangle_filled(inv_left, inv_right, y1, y2, color)
            if len(GameView.player_sprite.Inventory) == i+1 :
                item_name = GameView.player_sprite.Inventory[i]["short_name"]
            else:
                item_name = ""
            text = f"     {item_name}"
            arcade.draw_text(text, inv_left +10, (y1-y2)/ 2, arcade.color.ALLOY_ORANGE, 16)

        arcade.draw_lrtb_rectangle_outline(inv_left, inv_right, (self.window.height - 100), 175, BLACK, 3)

        for i in range(capacity_inventory):
            y1 = (self.window.height -100) - (i * field_height)
            y2 = y1 - field_height
            if i == self.selected_item - 1:
                arcade.draw_lrtb_rectangle_outline(
                    inv_left , inv_right, y1 , y2 , REDWOOD, 3
                )
        # Interfaz Hotbar
        for i in range (capacity_hotbar):
            start = 50 + i * (field_width + 25)
            if i < 1:
                arcade.draw_lrtb_rectangle_filled(50, 50 + field_width, 150, 50, WHITE)
                arcade.draw_lrtb_rectangle_outline(50, 50 + field_width, 150, 50, BLACK, 3)
                if self.selected_hotbar-1 == i and i == 0:
                    arcade.draw_lrtb_rectangle_outline(50, 50 + field_width, 150, 50, REDWOOD, 3)

            else:
                arcade.draw_lrtb_rectangle_filled(start, start + field_width, 150, 50 , WHITE)
                arcade.draw_lrtb_rectangle_outline(start, start + field_width, 150, 50 , BLACK, 3)
                if self.selected_hotbar-1 == i:
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
        texture = arcade.load_texture(":characters:inventory_picture.png")
        arcade.draw_scaled_texture_rectangle(center_x_sprite, center_y_sprite, texture, 0.35)

    def setup(self):
        pass
    def on_show_view(self):
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    def swap_item(self):
        if len(GameView.player_sprite.Inventory) < self.selected_item or len(GameView.player_sprite.hotbar) < self.selected_hotbar:
            print("no se puede")
        else:
            GameView.player_sprite.inventory[self.selected_item], GameView.player_sprite.hotbar [self.selected_hotbar] = GameView.player_sprite.hotbar [self.selected_hotbar], GameView.player_sprite.inventory[self.selected_item]

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
            self.selected_hotbar = 1
        elif symbol == arcade.key.KEY_7:
            self.selected_hotbar = 2
        elif symbol == arcade.key.KEY_8:
            self.selected_hotbar = 3

        elif symbol == arcade.key.SPACE:
            self.swap_item()

        close_inputs = [
            arcade.key.ESCAPE,
            arcade.key.I
        ]
        if symbol in close_inputs:
            self.window.show_view(self.window.views["game"])
