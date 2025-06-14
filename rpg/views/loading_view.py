"""
Loading screen
"""
import arcade

from rpg.configuracion_global import ConfiguracionGlobal
from rpg.draw_bar import draw_bar
from rpg.load_game_map import load_maps
from rpg.views.battle_view import BattleView
from rpg.views.game_view import GameView
from rpg.views.inventory_view import InventoryView
from rpg.views.main_menu_view import MainMenuView
from rpg.views.settings_view import SettingsView
from rpg.views.controls_view import ControlsView
from rpg.views.dialogue_view import DialogueView



class LoadingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.started = False
        self.progress = 0
        self.map_list = None
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        arcade.start_render()

        valor_brillo = 255 - int((ConfiguracionGlobal.brillo / 100) * 255)
        arcade.draw_lrtb_rectangle_filled(
            0, self.window.width, self.window.height, 0,
            (valor_brillo, valor_brillo, valor_brillo, 50)
        )

        arcade.draw_text(
            "Cargando la aventura ...",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        self.started = True
        draw_bar(
            current_amount=self.progress,
            max_amount=100,
            center_x=self.window.width / 2,
            center_y=50,
            width=self.window.width,
            height=20,
            color_a=arcade.color.ALMOND,
            color_b=arcade.color.ALLOY_ORANGE,
        )

    def setup(self):
        pass

    def on_update(self, delta_time: float):
        # Dictionary to hold all our maps
        if self.started:
            done, self.progress, self.map_list = load_maps()
            if done:
                self.window.views["game"] = GameView(self.map_list)
                self.window.views["game"].setup()
                self.window.views["inventory"] = InventoryView()
                self.window.views["inventory"].setup()
                self.window.views["main_menu"] = MainMenuView()
                self.window.views["settings"] = SettingsView()
                self.window.views["settings"].setup()
                self.window.views["controls"] = ControlsView()
                self.window.views["controls"].setup()
                self.window.views["battle"] = BattleView(self.window.views["game"])
                self.window.views["battle"].setup()
                self.window.views["dialogue"] = DialogueView(self.window.views["game"])


                self.window.show_view(self.window.views["game"])
