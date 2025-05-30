import arcade
from arcade.gui import UIManager, UIBoxLayout, UILabel, UIFlatButton, UIAnchorWidget

from rpg.configuracion_global import ConfiguracionGlobal


class MainSettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.etiqueta_volumen = None
        self.etiqueta_brillo = None
        self.boton_pantalla = None

        self.boton_style = {
            "font_name": ("Arial",),
            "font_size": 18,
            "font_color": arcade.color.WHITE,
            "bg_color": arcade.color.ALLOY_ORANGE,
            "border_color": arcade.color.ALMOND,
            "border_width": 4,
        }

    def setup(self):
        ConfiguracionGlobal.cargar()

    def on_show_view(self):
        self.ui_manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)
        self.setup_ui()

    def setup_ui(self):
        v_box = UIBoxLayout(space_between=30)

        titulo = UILabel(
            text="OPCIONES",
            font_size=32,
            font_name="Arial",
            text_color=arcade.color.ALLOY_ORANGE
        )
        v_box.add(titulo.with_space_around(bottom=40))

        # Volumen
        fila_volumen = UIBoxLayout(vertical=False, space_between=15)
        fila_volumen.add(UILabel(text="Volumen:", font_size=18, font_name="Arial", width=120))

        boton_menos_vol = UIFlatButton(text="-", width=40, style=self.boton_style)
        boton_menos_vol.on_click = self.disminuir_volumen
        fila_volumen.add(boton_menos_vol)

        self.etiqueta_volumen = UILabel(text=f"{ConfiguracionGlobal.volumen}%", font_size=18, font_name="Arial", width=50)
        fila_volumen.add(self.etiqueta_volumen)

        boton_mas_vol = UIFlatButton(text="+", width=40, style=self.boton_style)
        boton_mas_vol.on_click = self.aumentar_volumen
        fila_volumen.add(boton_mas_vol)

        v_box.add(fila_volumen)

        # Brillo
        fila_brillo = UIBoxLayout(vertical=False, space_between=15)
        fila_brillo.add(UILabel(text="Oscuridad:", font_size=18, font_name="Arial", width=120))

        boton_menos_bri = UIFlatButton(text="-", width=40, style=self.boton_style)
        boton_menos_bri.on_click = self.disminuir_brillo
        fila_brillo.add(boton_menos_bri)

        self.etiqueta_brillo = UILabel(text=f"{ConfiguracionGlobal.brillo}%", font_size=18, font_name="Arial", width=50)
        fila_brillo.add(self.etiqueta_brillo)

        boton_mas_bri = UIFlatButton(text="+", width=40, style=self.boton_style)
        boton_mas_bri.on_click = self.aumentar_brillo
        fila_brillo.add(boton_mas_bri)

        v_box.add(fila_brillo)

        # Botón volver
        volver_button = UIFlatButton(text="VOLVER", width=200, style=self.boton_style)
        volver_button.on_click = self.volver_al_menu
        v_box.add(volver_button.with_space_around(top=40))

        self.ui_manager.add(UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=v_box))

    def on_draw(self):
        self.clear()

        valor_brillo = 255 - int((ConfiguracionGlobal.brillo / 100) * 255)
        arcade.draw_lrtb_rectangle_filled(
            0, self.window.width, self.window.height, 0,
            (valor_brillo, valor_brillo, valor_brillo, 50)
        )

        self.ui_manager.draw()

    def on_hide_view(self):
        self.ui_manager.disable()

    # ---------------- MÉTODOS DE AJUSTE ----------------
    def aumentar_volumen(self, event):
        ConfiguracionGlobal.volumen = min(100, ConfiguracionGlobal.volumen + 10)
        self.actualizar_volumen()

    def disminuir_volumen(self, event):
        ConfiguracionGlobal.volumen = max(0, ConfiguracionGlobal.volumen - 10)
        self.actualizar_volumen()

    def actualizar_volumen(self):
        self.etiqueta_volumen.text = f"{ConfiguracionGlobal.volumen}%"

        # Actualizar volumen si hay música reproduciéndose
        if hasattr(self.window, "music_player") and self.window.music_player:
            self.window.music_player.volume = ConfiguracionGlobal.volumen / 100

        # Guardar configuración si procede
        ConfiguracionGlobal.guardar()


        # Si hay un reproductor de música activo, actualiza su volumen
        if hasattr(self.window, "music_player") and self.window.music_player:
            self.window.music_player.volume = ConfiguracionGlobal.volumen / 100

        ConfiguracionGlobal.guardar()

    def aumentar_brillo(self, event):
        ConfiguracionGlobal.brillo = min(100, ConfiguracionGlobal.brillo + 10)
        self.actualizar_brillo()

    def disminuir_brillo(self, event):
        ConfiguracionGlobal.brillo = max(0, ConfiguracionGlobal.brillo - 10)
        self.actualizar_brillo()

    def actualizar_brillo(self):
        self.etiqueta_brillo.text = f"{ConfiguracionGlobal.brillo}%"
        ConfiguracionGlobal.guardar()

    def volver_al_menu(self, event):
        self.ui_manager.disable()
        self.window.show_view(self.window.views["game_title"])
