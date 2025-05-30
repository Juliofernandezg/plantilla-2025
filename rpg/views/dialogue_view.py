import arcade

class DialogueView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

        self.dialogue_lines = []
        self.current_index = 0
        self.npc_name = ""

        self.text_box_width = 800
        self.text_box_height = 150

    def set_npc(self, npc_name, npc_data):
        """Cargar el NPC y sus diálogos"""
        self.npc_name = npc_name
        self.dialogue_lines = npc_data.get("dialogue", [])
        self.current_index = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)

    def on_draw(self):
        arcade.start_render()

        # Fondo de texto
        screen_width, screen_height = self.window.get_size()
        center_x = screen_width // 2
        bottom_y = 100
        arcade.draw_rectangle_filled(center_x, bottom_y + self.text_box_height // 2,
                                     self.text_box_width, self.text_box_height,
                                     arcade.color.BABY_BLUE_EYES)

        # Nombre del NPC
        arcade.draw_text(f"{self.npc_name}:", center_x - self.text_box_width // 2 + 20, bottom_y + 90,
                         arcade.color.BLACK, 16, bold=True)

        # Línea de diálogo
        if self.current_index < len(self.dialogue_lines):
            line = self.dialogue_lines[self.current_index]
            arcade.draw_text(line, center_x - self.text_box_width // 2 + 20, bottom_y + 50,
                             arcade.color.BLACK, 14, width=self.text_box_width - 40)

    def on_key_press(self, key, modifiers):
        if key in [arcade.key.SPACE, arcade.key.ENTER]:
            self.current_index += 1
            if self.current_index >= len(self.dialogue_lines):
                self.window.show_view(self.game_view)  # Volver al juego
