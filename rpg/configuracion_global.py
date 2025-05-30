import json

class ConfiguracionGlobal:
    volumen = 50
    brillo = 50
    pantalla_completa = False

    @staticmethod
    def guardar():
        with open("config.json", "w") as f:
            json.dump({
                "volumen": ConfiguracionGlobal.volumen,
                "brillo": ConfiguracionGlobal.brillo,
                "pantalla_completa": ConfiguracionGlobal.pantalla_completa
            }, f)

    @staticmethod
    def cargar():
        try:
            with open("config.json", "r") as f:
                data = json.load(f)
                ConfiguracionGlobal.volumen = data.get("volumen", 50)
                ConfiguracionGlobal.brillo = data.get("brillo", 50)
                ConfiguracionGlobal.pantalla_completa = data.get("pantalla_completa", False)
        except FileNotFoundError:
            pass