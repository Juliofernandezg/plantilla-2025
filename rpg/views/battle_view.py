import arcade
import random
import rpg.constants as constants
from rpg.configuracion_global import ConfiguracionGlobal
from rpg.views.game_view import GameView
from rpg.sprites import player_sprite
from rpg.views.game_over_view import GameOver


class BattleView(arcade.View):
    def __init__(self, GameView):
        super().__init__()
        self.GameView = GameView

        self.player_sprite = GameView.player_sprite

        self.return_position = None

        self.enemy_name = None
        self.enemy_data = {}
        self.enemy_sprite = None
        self.intro_index = 0
        self.battle_state = "intro"  # intro, player_turn, enemy_turn, finished
        self.battle_log = []

        GameView.gain_exp(0)
        GameView.apply_damage(0)
        GameView.use_mana(0)
        GameView.apply_heal(0)

        self.enemy_hp = 100

        # Compatibilidad
        self.player_hp = self.player_sprite.current_health
        self.player_mana = self.player_sprite.current_mana
        self.max_mana = self.player_sprite.max_mana

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
                file_name = image_path,
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

    def draw_linkillo(self):
        # PICTURE
        center_x_sprite = (self.window.width / 2) + 400
        center_y_sprite = (self.window.height / 2) + 70

        texture = arcade.load_texture(":characters:linkillo_picture.png")
        arcade.draw_scaled_texture_rectangle(center_x_sprite, center_y_sprite, texture, 0.3)

        # STATS - Usando los valores actuales de PlayerSprite
        arcade.draw_text(
            f"linkillo HP: {self.player_sprite.current_health}/{self.player_sprite.max_health}",
            (self.window.width / 2) + 320,
            (self.window.height / 2) - 200,
            arcade.color.ALLOY_ORANGE, 20
        )
        arcade.draw_text(
            f"Mana: {self.player_sprite.current_mana}/{self.player_sprite.max_mana}",
            (self.window.width / 2) + 320,
            (self.window.height / 2) - 220,
            arcade.color.DARK_BLUE, 18
        )

    def draw_enemy(self, name):
        # PICTURE
        if name == "skeleton":
            center_x_sprite = (self.window.width / 2) - 400
            center_y_sprite = (self.window.height / 2) + 70

            texture = arcade.load_texture(":characters:skeleton_picture.png")
            arcade.draw_scaled_texture_rectangle(center_x_sprite, center_y_sprite, texture, 0.3)

        if name == "calabaza":
            center_x_sprite = (self.window.width / 2) - 400
            center_y_sprite = (self.window.height / 2) + 70

            texture = arcade.load_texture(":characters:calabaza_picture.png")
            arcade.draw_scaled_texture_rectangle(center_x_sprite, center_y_sprite, texture, 0.3)

        if name == "novia":
            center_x_sprite = (self.window.width / 2) - 400
            center_y_sprite = (self.window.height / 2) + 70

            texture = arcade.load_texture(":characters:novia_picture.png")
            arcade.draw_scaled_texture_rectangle(center_x_sprite, center_y_sprite, texture, 0.3)

        if name == "mago":
            center_x_sprite = (self.window.width / 2) - 400
            center_y_sprite = (self.window.height / 2) + 70

            texture = arcade.load_texture(":characters:mago_picture.png")
            arcade.draw_scaled_texture_rectangle(center_x_sprite, center_y_sprite, texture, 0.3)

        if name == "jefe":
            center_x_sprite = (self.window.width / 2) - 400
            center_y_sprite = (self.window.height / 2) + 70

            texture = arcade.load_texture(":characters:jefe_picture.png")
            arcade.draw_scaled_texture_rectangle(center_x_sprite, center_y_sprite, texture, 0.3)

        # STATS
        arcade.draw_text(f"{name} HP: {self.enemy_hp}", (self.window.width / 2) - 500,
                         (self.window.height / 2) - 200,
                         arcade.color.ALLOY_ORANGE, 20)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        arcade.start_render()

        valor_brillo = 255 - int((ConfiguracionGlobal.brillo / 100) * 255)
        arcade.draw_lrtb_rectangle_filled(
            0, self.window.width, self.window.height, 0,
            (valor_brillo, valor_brillo, valor_brillo, 50)
        )

        self.draw_linkillo()

        name = self.enemy_data.get("name", "???")
        self.draw_enemy(name)

        if not self.enemy_data:
            arcade.draw_text("Error: enemigo no cargado.", self.window.width / 2, self.window.height / 2,
                             arcade.color.RED, 24, anchor_x="center")
            return

        if self.enemy_sprite:
            self.enemy_sprite.draw()

        if self.battle_state == "intro" and self.enemy_data.get("intro"):
            if self.intro_index < len(self.enemy_data["intro"]):
                text = self.enemy_data["intro"][self.intro_index]
                arcade.draw_text(text, self.window.width / 2, self.window.height - 70,
                                 arcade.color.ALLOY_ORANGE, 40, anchor_x="center")

        elif self.battle_state == "player_turn":
            arcade.draw_text("[A] Atacar  [M] Magia  [I] Ítem  [F] Huir",
                             self.window.width / 2, 70, arcade.color.ALLOY_ORANGE, 40, anchor_x="center")

        elif self.battle_state == "enemy_turn":
            arcade.draw_text("Turno del enemigo...", self.window.width / 2, 100,
                             arcade.color.ALLOY_ORANGE, 40, anchor_x="center")

        elif self.battle_state == "finished":
            if self.enemy_hp <= 0:

                # Gana experiencia
                GameView.gain_exp(self, 1)

                arcade.draw_text("¡COMBATE FINALIZADO!", self.window.width / 2, 80,
                                 arcade.color.ALLOY_ORANGE, 40, anchor_x="center")
                arcade.draw_text("Disfruta de esa XP galán", (self.window.width / 2), 30,
                                 arcade.color.ALLOY_ORANGE, 30, anchor_x="center")

                # Añade un pequeño retraso antes de volver al juego
                arcade.schedule(self.return_to_game,3.0)

            elif self.player_hp <= 0:
                arcade.draw_text("¡HAS SIDO DERROTADO!", self.window.width / 2, 70,
                                 arcade.color.ALLOY_ORANGE, 40, anchor_x="center")

                # Añade un pequeño retraso antes de volver al juego
                arcade.schedule(self.return_to_game,3.0)

        elif self.battle_state == "finished_huir":
            arcade.draw_text("¡LINKILLO HA HUIDO, QUÉ COBARDE!", self.window.width / 2, 70,
                             arcade.color.ALLOY_ORANGE, 40, anchor_x="center")

            # Añade un pequeño retraso antes de volver al juego
            arcade.schedule(self.return_to_game,3.0)

        # BATTLE LOG
        visible_lines = self.battle_log[-6:] if len(self.battle_log) > 6 else self.battle_log
        for i, line in enumerate(reversed(visible_lines)):
            arcade.draw_text(line, (self.window.width / 2) - 230,
                             (self.window.height / 2) - 100 + i * 25,
                             arcade.color.ALLOY_ORANGE, 20)

    def return_to_game(self, delta_time):
        """Función para volver al juego después de huir o terminar batalla"""
        arcade.unschedule(self.return_to_game)
        if self.player_hp <= 0:
            self.window.show_view(self.window.views["game_over"])
        else:
            self.window.show_view(self.window.views["game"])

    def use_mana(self, amount):
        if self.player_mana >= amount:
            self.player_mana -= amount
            self.player_sprite.current_mana = self.player_mana
            return True
        return False


    def on_key_press(self, symbol: int, modifiers: int):
        if not self.enemy_data:
            return

        if self.battle_state == "intro":
            self.intro_index += 1
            if self.intro_index >= len(self.enemy_data.get("intro", [])):
                self.battle_state = "player_turn"
            return

        if self.battle_state == "player_turn":
            if symbol == arcade.key.A:   # Atacar
                damage = random.randint(10, 20)
                self.enemy_hp -= damage
                self.battle_log.append(f"Linkillo atacó e hizo {damage} de daño.")
                self.check_victory()
                if self.battle_state != "finished":
                    self.battle_state = "enemy_turn"
                    arcade.schedule(self.enemy_attack, 1.0)

            elif symbol == arcade.key.M:   # Magia
                if self.player_mana >= 10:
                    damage = random.randint(20, 30)
                    self.enemy_hp -= damage

                    mana = 10
                    self.use_mana(mana)
                    self.battle_log.append(f"Linkillo usó magia: {damage} de daño (10 MP).")
                    self.check_victory()
                    if self.battle_state != "finished":
                        self.battle_state = "enemy_turn"
                        arcade.schedule(self.enemy_attack, 1.0)
                else:
                    self.battle_log.append("¡No tienes suficiente maná!")

            elif symbol == arcade.key.I:   # Item
                player_sprite = self.window.views["game"].player_sprite
                if player_sprite.hotbar:
                    heal = 20
                    self.player_hp += heal
                    self.player_hp = min(self.player_hp, 100)
                    GameView.apply_heal(self, heal)

                    item = player_sprite.hotbar.pop(0)
                    self.battle_log.append(f"Usaste {item['short_name']}, recuperaste {heal} HP.")
                else:
                    self.battle_log.append("No tienes ítems disponibles.")

            elif symbol == arcade.key.F:
                huir = random.randint(0,2)
                if huir == 0:
                    self.battle_log.append("Linkillo echa a correr")
                    self.battle_state = "finished_huir"
                    arcade.unschedule(self.enemy_attack)
                else:
                    self.battle_log.append("Linkillo no se decide")

                    self.check_victory()
                    if self.battle_state != "finished":
                        self.battle_state = "enemy_turn"
                        arcade.schedule(self.enemy_attack, 1.0)


    def apply_damage(self, amount):
        self.player_hp = max(0, self.player_hp - amount)
        self.player_sprite.current_health = self.player_hp

    def enemy_attack(self, delta_time):
        if self.battle_state != "enemy_turn":
            return

        damage = random.randint(8, 18)

        self.apply_damage(damage)

        self.battle_log.append(f"{self.enemy_data.get('name', '???')} atacó (-{damage} HP)")
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
            self.battle_log.append("Linkillo no se siente bien...")
            self.battle_state = "finished"

    def on_update(self, delta_time: float):
        self.window.views["game_over"] = GameOver()
        self.window.views["game_over"].setup()