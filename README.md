# 🐾 Funkelin

**Funkelin** es una plataforma web ligera y modular para la gestión y rastreo de mascotas. Desarrollada en Python con Flask (backend) y HTML/JavaScript (frontend), permite listar, agregar y visualizar mascotas a través de una API REST sencilla y funcional.

---

## 🚀 Tecnologías utilizadas

- **Backend:** Python + Flask + SQLAlchemy
- **Base de Datos:** SQLite
- **Frontend:** HTML + JavaScript (Fetch API)
- **ORM:** SQLAlchemy

---

## 📁 Estructura del proyecto


---

## 🔧 Funcionalidades actuales

- Endpoint `/api/mascotas` para obtener mascotas
- Backend modularizado (routes, models, services)
- Persistencia en SQLite con ORM
- Frontend conectado al backend vía Fetch API
- Endpoint de prueba para agregar mascotas

---

## 📦 Instalación local

```bash
git clone https://github.com/amoamarlene13666/Funkelin.git
cd Funkelin/backend
python -m venv venv
venv\Scripts\activate
pip install flask sqlalchemy
python app.py
