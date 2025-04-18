from models.mascota import Mascota, db  # Asegúrate de importar correctamente la base de datos

def agregar_mascota(nombre, tipo, edad):
    """Agrega una nueva mascota a la base de datos."""
    # Crear una nueva instancia de Mascota
    nueva_mascota = Mascota(nombre=nombre, tipo=tipo, edad=edad)
    db.session.add(nueva_mascota)  # Añadir al registro en la base de datos
    db.session.commit()  # Guardar cambios en la base de datos
    return nueva_mascota

def obtener_mascotas():
    """Devuelve la lista completa de mascotas desde la base de datos."""
    # Consultar todas las mascotas en la base de datos
    return Mascota.query.all()

def eliminar_mascota(id):
    """Elimina una mascota de la base de datos por su ID."""
    # Buscar la mascota por ID
    mascota = Mascota.query.get(id)
    if mascota is None:
        raise ValueError(f"No se encontró ninguna mascota con ID: {id}")
    db.session.delete(mascota)  # Eliminar el registro de la base de datos
    db.session.commit()  # Guardar cambios en la base de datos
    return True