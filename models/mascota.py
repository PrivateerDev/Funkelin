from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Inicialización de SQLAlchemy en este archivo

class Mascota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    tipo = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "edad": self.edad
        }