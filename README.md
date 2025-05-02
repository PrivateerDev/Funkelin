
# 🐾 Funkelin

**Funkelin** es un sistema modular para gestionar mascotas con una arquitectura cliente-servidor construida sobre Flask (Python) y un frontend en JavaScript puro. Se enfoca en **programación defensiva**, **validación robusta** y una experiencia de usuario dinámica.

---

## 📂 Estructura del Proyecto

```

Funkelin/
│── backend/
│   ├── models/
│   │   ├── mascota.py            # 🚀 Modelo de mascotas con validaciones robustas
│   ├── routes/
│   │   ├── mascotas.py           # 🚀 API REST con programación defensiva
│   ├── services/
│   │   ├── mascota\_service.py    # 🚀 Gestión eficiente de datos en SQLite
│   ├── app.py                    # 🚀 Configuración central del servidor Flask
│── frontend/
│   ├── index.html                # 🚀 Interfaz visual con UI mejorada
│   ├── app.js                    # 🚀 Manejo de interacciones y comunicación con el backend
│   ├── styles.css                # 🚀 Estilos optimizados para mejor experiencia de usuario
│── README.md                     # 🚀 Documentación del proyecto

```

---

## 🛡️ Programming Defensivo y Robustez en Funkelin

### 📦 Backend (Python - Flask API)

- ✅ Validación estricta de entrada con `assert`
- ✅ Postcondiciones tras operaciones CRUD (e.g. `id` no `None`)
- ✅ Manejo de errores con `try-except`, `abort(404)`, y `RuntimeError`
- ✅ Control de transacciones (`db.session.begin()` + `rollback()` en fallos)
- ✅ Conversión segura de tipos (`edad` convertida a entero)
- ✅ CORS restringido únicamente a `/api/*`
- ✅ Integridad de datos reforzada en modelos (`mascota.py`)

### ⚙️ Configuración del Servidor (`app.py`)

- ✅ Inicialización segura de la app (`db.init_app`, registro ordenado de rutas)
- ✅ Verificación de entorno (`FLASK_ENV`) y base de datos en ejecución
- ✅ Uso controlado de `app.app_context()` para operaciones críticas

---

### 🌐 Frontend (JavaScript + HTML + CSS)

- ✅ Verificación del DOM antes de acceder a elementos (`getElementById`)
- ✅ Sanitización de entradas de usuario (`sanitizarTexto`)
- ✅ Validación en tiempo real (nombre, especie, edad)
- ✅ Manejo robusto de errores en `fetch()` con `try-catch`
- ✅ Actualización dinámica de la interfaz sin recarga (`fetchMascotas`)
- ✅ Feedback visual mediante `alert`, `console.log` y `console.assert`
- ✅ UI accesible y responsiva (`styles.css`, mejoras de diseño)

---

## 📌 Resultado Final

Funkelin es un sistema **robusto, seguro y mantenible**, con validaciones **end-to-end** desde la entrada del usuario hasta la persistencia en base de datos. La programación defensiva garantiza que tanto el backend como el frontend manejen errores de forma controlada, brindando una experiencia confiable.
