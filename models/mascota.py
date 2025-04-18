from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Mascota(Base):
    __tablename__ = 'mascotas'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    especie = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "especie": self.especie
        }
