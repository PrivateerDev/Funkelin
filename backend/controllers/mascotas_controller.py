# controllers/mascotas_controller.py

mascotas_registradas = []  # almacenamiento temporal


class Mascota:
    def __init__(self, nombre, especie):
        self.nombre = nombre
        self.especie = especie

    def to_dict(self):
        return {"nombre": self.nombre, "especie": self.especie}


def agregar_mascota(nombre, especie):
    nueva = Mascota(nombre, especie)
    mascotas_registradas.append(nueva)
    return nueva


def obtener_mascotas():
    return mascotas_registradas
