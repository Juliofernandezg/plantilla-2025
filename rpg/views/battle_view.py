import arcade
import random
import rpg.constants as constants


class BattleView(arcade.View):
    def __init__(self):
        super().__init__()
        self.return_position = None

        self.enemy_name = None
        self.enemy_data = {}
        self.enemy_sprite = None
        self.intro_index = 0
        self.battle_state = "intro"  # intro, player_turn, enemy_turn, finished
        self.battle_log = []

        self.player_hp = 100
        self.enemy_hp = 100
        self.player_mana = 50
        self.max_mana = 50

        arcade.set_background_color(arcade.color.ALMOND)

    def setup(self):
        pass
    def set_enemy(self, npc_name, npc_data):
        """Cargar enemigo para batalla"""
        self.enemy_name = npc_name
        self.enemy_data = npc_data or {}

        # Nombre, vida, imagen, intro...
        self.enemy_hp = self.enemy_data.get("hp", 100)
        image_path = arcade.load_texture(":characters:Boss/prueba.png")

        try:
            # Recorta solo un frame frontal (por ejemplo, frame 9)
            texture = arcade.load_spritesheet(
                file_name=image_path,
                sprite_width=16,
                sprite_height=16,
                columns=3,
                count=12
            )[9]  # Ajusta según corresponda
        except Exception as e:
            print(f"[ERROR] Al cargar spritesheet: {e}")
            texture = None

        self.enemy_sprite = arcade.Sprite(center_x=self.window.width // 2,
                                          center_y=self.window.height // 2 + 100,
                                          scale=3)
        if texture:
            self.enemy_sprite.texture = texture

        self.intro_index = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        arcade.start_render()

        # Interfaz Personaje(WIP)
        center_x_sprite = (self.window.width - ((self.window.width / 2) + 100)) / 2 + ((self.window.width / 2) + 100)
        center_y_sprite = self.window.height / 2

        texture = arcade.load_texture(":characters:inventory_picture.png")
        arcade.draw_scaled_texture_rectangle(center_x_sprite, center_y_sprite, texture, 0.35)

        if not self.enemy_data:
            arcade.draw_text("Error: enemigo no cargado.", self.window.width / 2, self.window.height / 2,
                             arcade.color.RED, 24, anchor_x="center")
            return

        if self.enemy_sprite:
            self.enemy_sprite.draw()

        name = self.enemy_data.get("name", "???")
        arcade.draw_text(f"Linkillo HP: {self.player_hp}", 30, self.window.height - 50, arcade.color.ALLOY_ORANGE, 20)
        arcade.draw_text(f"Mana: {self.player_mana}/{self.max_mana}", 30, self.window.height - 80, arcade.color.DARK_BLUE, 18)
        arcade.draw_text(f"{name} HP: {self.enemy_hp}", 30, self.window.height - 110, arcade.color.ALLOY_ORANGE, 20)

        if self.battle_state == "intro" and self.enemy_data.get("intro"):
            if self.intro_index < len(self.enemy_data["intro"]):
                text = self.enemy_data["intro"][self.intro_index]
                arcade.draw_text(text, self.window.width / 2, self.window.height - 200,
                                 arcade.color.ALLOY_ORANGE, 50, anchor_x="center")

        elif self.battle_state == "player_turn":
            arcade.draw_text("Tu turno: [A] Atacar  [M] Magia  [I] Ítem  [F] Huir",
                             self.window.width / 2, 100, arcade.color.ALLOY_ORANGE, 40, anchor_x="center")

        elif self.battle_state == "enemy_turn":
            arcade.draw_text("Turno del enemigo...", self.window.width / 2, 100,
                             arcade.color.ALLOY_ORANGE, 40, anchor_x="center")

        elif self.battle_state == "finished":
            arcade.draw_text("¡COMBATE FINALIZADO!", self.window.width / 2, 100,
                             arcade.color.ALLOY_ORANGE, 50, anchor_x="center")

            self.window.show_view(self.window.views["game"])

        # BATTLE LOG
        for i, line in enumerate(self.battle_log[-4:]):
            arcade.draw_text(line, 30, 200 + i * 25, arcade.color.ALLOY_ORANGE, 20)

    def on_key_press(self, symbol: int, modifiers: int):
        if not self.enemy_data:
            return

        if self.battle_state == "intro":
            self.intro_index += 1
            if self.intro_index >= len(self.enemy_data.get("intro", [])):
                self.battle_state = "player_turn"
            return

        if self.battle_state == "player_turn":
            if symbol == arcade.key.A:
                damage = random.randint(10, 20)
                self.enemy_hp -= damage
                self.battle_log.append(f"Linkillo atacó e hizo {damage} de daño.")
                self.check_victory()
                if self.battle_state != "finished":
                    self.battle_state = "enemy_turn"
                    arcade.schedule(self.enemy_attack, 1.0)

            elif symbol == arcade.key.M:
                if self.player_mana >= 15:
                    damage = random.randint(20, 30)
                    self.enemy_hp -= damage
                    self.player_mana -= 15
                    self.battle_log.append(f"Linkillo lanzó magia: {damage} de daño (15 MP).")
                    self.check_victory()
                    if self.battle_state != "finished":
                        self.battle_state = "enemy_turn"
                        arcade.schedule(self.enemy_attack, 1.0)
                else:
                    self.battle_log.append("¡No tienes suficiente maná!")

            elif symbol == arcade.key.I:
                player_sprite = self.window.views["game"].player_sprite
                if player_sprite.hotbar:
                    heal = random.randint(20, 30)
                    self.player_hp += heal
                    self.player_hp = min(self.player_hp, 100)
                    item = player_sprite.hotbar.pop(0)
                    self.battle_log.append(f"Usaste {item['short_name']}, recuperaste {heal} HP.")
                else:
                    self.battle_log.append("No tienes ítems disponibles.")

            elif symbol == arcade.key.F:
                self.battle_log.append("¡LINKILLO HA HUIDO DEL COMBATE, QUÉ COBARDE!")
                self.battle_state = "finished"
                arcade.unschedule(self.enemy_attack)

        elif symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["main_menu"])

    def enemy_attack(self, delta_time):
        if self.battle_state != "enemy_turn":
            return

        damage = random.randint(8, 18)
        self.player_hp -= damage
        self.battle_log.append(f"{self.enemy_data.get('name', '???')} atacó y causó {damage} de daño.")
        self.check_defeat()

        if self.battle_state != "finished":
            self.battle_state = "player_turn"

        arcade.unschedule(self.enemy_attack)

    def check_victory(self):
        if self.enemy_hp <= 0:
            self.battle_log.append(f"¡Has derrotado a {self.enemy_data.get('name', 'enemigo')}!")
            self.battle_state = "finished"
            if hasattr(self.window.views["game"], "register_defeated_enemy"):
                self.window.views["game"].register_defeated_enemy(self.enemy_name)
                self.window.views["game"].remove_enemy_sprite(self.enemy_name)

    def check_defeat(self):
        if self.player_hp <= 0:
            self.battle_log.append("¡HAS SIDO DERROTADO!")
            self.battle_state = "finished"
