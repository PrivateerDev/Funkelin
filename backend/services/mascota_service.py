from models.mascota import (
    Mascota,
    db,
)  # Asegúrate de importar correctamente la base de datos


def agregar_mascota(nombre: str, tipo: str, edad: int) -> Mascota:
    """Agrega una nueva mascota a la base de datos."""
    # Validar datos de entrada
    if not nombre or not tipo or edad <= 0:
        raise ValueError("Los datos proporcionados son inválidos: nombre, tipo y edad son requeridos y deben ser válidos.")

    # Crear una nueva instancia de Mascota
    nueva_mascota = Mascota(nombre=nombre, tipo=tipo, edad=edad)
    db.session.add(nueva_mascota)  # Añadir al registro en la base de datos
    db.session.commit()  # Guardar cambios en la base de datos
    return nueva_mascota


def obtener_mascotas() -> list[Mascota]:
    """Devuelve la lista completa de mascotas desde la base de datos."""
    # Consultar todas las mascotas en la base de datos
    return Mascota.query.all()


def eliminar_mascota(id: int) -> bool:
    """Elimina una mascota de la base de datos por su ID."""
    # Validar el ID de entrada
    if id <= 0:
        raise ValueError("El ID proporcionado no es válido.")

    # Buscar la mascota por ID
    mascota = Mascota.query.get(id)
    if mascota is None:
        raise ValueError(f"No se encontró ninguna mascota con ID: {id}")
    db.session.delete(mascota)  # Eliminar el registro de la base de datos
    db.session.commit()  # Guardar cambios en la base de datos
    return True
