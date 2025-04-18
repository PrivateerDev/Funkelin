from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.mascota import Base, Mascota

# Conexión a SQLite (archivo local)
engine = create_engine('sqlite:///funkelin.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Crear la tabla si no existe
Base.metadata.create_all(engine)

def obtener_mascotas():
    return session.query(Mascota).all()

def agregar_mascota(nombre, especie):
    nueva = Mascota(nombre=nombre, especie=especie)
    session.add(nueva)
    session.commit()
    return nueva
