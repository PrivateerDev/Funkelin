from models import db  # Importar db desde models/__init__.py

class Mascota(db.Model):
    """Modelo para representar una mascota en la base de datos."""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    tipo = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """Convierte la instancia de Mascota a un diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "edad": self.edad
        }