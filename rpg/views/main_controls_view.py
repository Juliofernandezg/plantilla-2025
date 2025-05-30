import arcade
import arcade.gui

from rpg.configuracion_global import ConfiguracionGlobal


class ControlsUI:
    def __init__(self, manager, button_style=None):
        self.manager = manager
        self.v_box = arcade.gui.UIBoxLayout()

        if not button_style:
            button_style = {
                "font_name": ("Arial",),
                "font_size": 18,
                "font_color": arcade.color.WHITE,
                "bg_color": arcade.color.ALLOY_ORANGE,
                "border_color": arcade.color.ALMOND,
                "border_width": 4,
            }

        # Lista ordenada de controles
        controls_list = [
            "W / ↑ : Ir pa riba",
            "A / ← : Ir pa la izquierda",
            "S / ↓ : Ir pa bajo",
            "D / → : Ir pa la derecha",
            " ",
            "E: Buscar",
            "I: Inventario",
            "L: Encender luz",
            " ",
            "ESC : Pausa / Volver"
        ]

        # Añadir cada control como una etiqueta separada
        for control in controls_list:
            label = arcade.gui.UILabel(
                text=control,
                text_color=arcade.color.ALLOY_ORANGE,
                font_size=28
            )
            self.v_box.add(label.with_space_around(bottom=16))

        # Anclar layout
        self.anchor = arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            align_y=-60,  # set v.box 60 pixels down
            child=self.v_box
        )
        self.manager.add(self.anchor)

    def destroy(self):
        """Eliminar los widgets del manager"""
        self.manager.remove(self.anchor)


class MainControlsView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.controls_ui = None

    def setup(self):
        pass

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

        # Crear la UI de controles y asignar callback al botón
        self.controls_ui = ControlsUI(self.manager)

    def on_draw(self):
        self.clear()
        self.manager.draw()

        valor_brillo = 255 - int((ConfiguracionGlobal.brillo / 100) * 255)
        arcade.draw_lrtb_rectangle_filled(
            0, self.window.width, self.window.height, 0,
            (valor_brillo, valor_brillo, valor_brillo, 50)
        )

        arcade.draw_text(
            "CONTROLS",
            self.window.width / 2,
            self.window.height - 80,
            arcade.color.ALLOY_ORANGE,
            48,
            anchor_x="center",
        )

    def on_hide_view(self):
        self.manager.disable()
        self.controls_ui.destroy()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["game_title"])