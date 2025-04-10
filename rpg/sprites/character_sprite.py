"""
Animated sprite for characters that walk around.
"""


import arcade

from enum import Enum
from rpg.constants import SPRITE_SIZE

Direction = Enum("Direction", "DOWN LEFT RIGHT UP")

SPRITE_INFO = {
    Direction.DOWN: [0, 1, 2],
    Direction.LEFT: [3, 4, 5],
    Direction.RIGHT: [6, 7, 8],
    Direction.UP: [9, 10, 11],
}


class CharacterSprite(arcade.Sprite):
    def __init__(self, sheet_name):
        super().__init__()
        self.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width=SPRITE_SIZE,
            sprite_height=SPRITE_SIZE,
            columns=3,
            count=12,
        )
        self.should_update = 0
        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]
        self.inventory = []

        # Estadísticas del jugador
        self.max_health = 100
        self.health = 100
        self.attack = 10
        self.exp = 0
        self.mana = 50
        self.level = 1
        self.exp_to_next_level = 100

    def take_damage(self, amount):
        """
        Reduce la vida del jugador.

        :param amount: Cantidad de daño recibido.
        """
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        """
        Aumenta la vida del jugador.

        :param amount: Cantidad de vida recuperada.
        """
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def use_mana(self, amount):
        """
        Consume mana del jugador.

        :param amount: Cantidad de mana a consumir.
        :return: True si hay suficiente mana, False en caso contrario.
        """
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False

    def gain_exp(self, amount):
        """
        Aumenta la experiencia del jugador.

        :param amount: Cantidad de experiencia ganada.
        """
        self.exp += amount
        if self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        """
        Sube de nivel al jugador y mejora sus estadísticas.
        """
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        self.max_health += 20
        self.health = self.max_health
        self.attack += 5
        self.mana += 10

    def draw_health_bar(self):
        """
        Dibuja la barra de vida en la esquina superior izquierda de la pantalla.
        """
        health_bar_width = 200
        health_bar_height = 20
        health_percentage = self.health / self.max_health
        arcade.draw_rectangle_filled(health_bar_width / 2 + 10, arcade.get_window().height - 20, health_bar_width,
                                     health_bar_height, arcade.color.GRAY)
        arcade.draw_rectangle_filled(health_bar_width / 2 + 10, arcade.get_window().height - 20,
                                     health_bar_width * health_percentage, health_bar_height, arcade.color.RED)

    def on_update(self, delta_time):
        if not self.change_x and not self.change_y:
            return

        # self.center_x += self.change_x
        # self.center_y += self.change_y

        if self.should_update <= 3:
            self.should_update += 1
        else:
            self.should_update = 0
            self.cur_texture_index += 1

        direction = Direction.LEFT
        slope = self.change_y / (self.change_x + 0.0001)
        if abs(slope) < 0.8:
            if self.change_x > 0:
                direction = Direction.RIGHT
            else:
                # technically not necessary, but for readability
                direction = Direction.LEFT
        else:
            if self.change_y > 0:
                direction = Direction.UP
            else:
                direction = Direction.DOWN

        if self.cur_texture_index not in SPRITE_INFO[direction]:
            self.cur_texture_index = SPRITE_INFO[direction][0]

        self.texture = self.textures[self.cur_texture_index]
