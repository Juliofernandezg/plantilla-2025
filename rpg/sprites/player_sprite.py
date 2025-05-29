import arcade

from rpg.sprites.character_sprite import CharacterSprite


class PlayerSprite(CharacterSprite):
    def __init__(self, sheet_name):
        super().__init__(sheet_name)

        # Atributos de stats
        self.max_health = 100
        self.current_health = 100
        self.max_mana = 50
        self.current_mana = 50
        self.experience = 0
        self.max_experience = 500
        self.level = 1

        # Regeneración de mana
        self.mana_regen_timer = 0
        self.mana_regen_rate = 1

        # Hotbar e inventario
        self.hotbar = []
        self.Inventory = []

        # Sonidos
        self.sound_update = 0
        self.footstep_sound = arcade.load_sound(":sounds:footstep00.wav")


    def take_damage(self, amount):
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0

    def heal(self, amount):
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def use_mana(self, amount):
        self.current_mana -= amount
        if self.current_mana < 0:
            self.current_mana = 0

    def heal_mana(self, amount):
        self.current_mana += amount
        if self.current_mana > self.max_mana:
            self.current_mana = self.max_mana

    def gain_exp(self, amount):
        self.experience += amount
        if self.experience >= self.max_experience:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.max_experience = int(self.max_experience * 1.3)
        self.max_health += 20
        self.current_health = self.max_health
        self.max_mana += 10
        self.current_mana = self.max_mana

    def update_mana_regen(self, delta_time):
        """Actualiza la regeneración de maná"""
        self.mana_regen_timer += delta_time
        if self.mana_regen_timer >= 1.0:  # Cada segundo
            self.mana_regen_timer = 0
            self.heal_mana(self.mana_regen_rate)


    def on_update(self, delta_time):
        super().on_update(delta_time)

        # Regeneración de maná (solo fuera de combate)
        if hasattr(self, 'player_sprite'):
            self.mana_regen_timer += delta_time
            if self.mana_regen_timer >= 1.0:  # Cada segundo
                self.mana_regen_timer = 0
                if self.player_sprite.current_mana < self.player_sprite.max_mana:
                    self.player_sprite.heal_mana(1)  # Recupera 1 punto


        if not self.change_x and not self.change_y:
            self.sound_update = 0
            return

        if self.should_update > 3:
            self.sound_update += 1

        if self.sound_update >= 3:
            arcade.play_sound(self.footstep_sound)
            self.sound_update = 0


