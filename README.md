
---

## 📊 **Tabla comparativa global de niveles de logging aplicados en Funkelin. Aplicado a todo el proyecto, elegí estos para muestra:**

| **Módulo**           | **DEBUG**                                                                                                           | **INFO**                                                                                     | **WARNING**                                                                                | **ERROR**                                                                                                |
| -------------------- | ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| `app.py` (principal) | Inicio de configuración y creación de tablas<br>Función `debug()`                                                   | Configuración de BD<br>Inicialización<br>Blueprints<br>Inicio de Flask<br>Consultas exitosas | Ausencia de mascotas en `/api/debug`                                                       | Fallo en creación de tablas<br>Registro de rutas<br>Errores en consulta a BD                             |
| `Mascota` (modelo)   | Inicio y fin de `__init__`<br>Métodos de validación<br>`to_dict()`                                                  | Mascota creada exitosamente                                                                  | Entradas inválidas (nombre, tipo, edad)                                                    | Fallos al instanciar con datos incorrectos (ValueError)                                                  |
| `routes/mascotas.py` | Inicialización del blueprint<br>Sanitización de texto<br>Ejecución de endpoints                                     | Pruebas (`/test`), recuperación, alta y baja de mascotas exitosas                            | POST vacío<br>Edad inválida<br>Validaciones fallidas<br>Eliminación de mascota inexistente | Excepciones en GET/POST/DELETE<br>Errores en base de datos                                               |
| `mascota_service.py` | Inicio de funciones clave (`agregar`, `obtener`, `eliminar`)<br>Datos de entrada y proceso                          | Confirmaciones de alta, baja y consulta de mascotas                                          | Datos inválidos<br>Eliminación de mascota inexistente                                      | Fallos en inserción o consulta SQL<br>Errores lógicos                                                    |
| `main.js` (frontend) | Sanitización de entradas<br>Inicio de funciones (`fetchMascotas`, `eliminarMascota`, etc.)<br>Carga inicial del DOM | Éxito en solicitudes GET/POST/DELETE<br>Actualización del DOM<br>Reseteo de formulario       | Validaciones de entrada fallidas<br>ID no válido<br>Elementos del DOM no encontrados       | Fallos en `fetch` (backend inaccesible, errores HTTP)<br>Error crítico al cargar mascotas o enviar datos |

---

### ✅ **Resumen consolidado para tu reporte de práctica**

El sistema Funkelin demuestra una aplicación **consistente, estructurada y eficaz** del sistema de logging en todos sus componentes:

* **DEBUG** se utiliza para **monitorear procesos internos**, ideal para pruebas y debugging.
* **INFO** registra operaciones exitosas o esperadas, que confirman el funcionamiento correcto del sistema.
* **WARNING** indica **anomalías leves** que no interrumpen el sistema, pero que ayudan a mejorar su robustez frente a errores comunes de entrada o lógica.
* **ERROR** permite detectar fallos graves que requieren atención inmediata, ya sean del lado del servidor (backend), modelo de datos o del cliente (frontend).

El enfoque unificado en todos los módulos garantiza **trazabilidad completa**, facilidad de **mantenimiento**, y capacidad de **respuesta ante incidentes** tanto en entornos de desarrollo como en producción.

---

---

### 🧩 **Aplicación de niveles de logging en `app.py`**

| **Nivel de log** | **Ubicación / Acción registrada**                                                                                                                                                                                                                                                                                    | **Justificación**                                                                                                                         |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **DEBUG**        | - Inicio de la configuración principal<br>- Inicio de la creación de tablas<br>- Ejecución de la función `debug()`                                                                                                                                                                                                   | Permite rastrear paso a paso la inicialización de la aplicación y el proceso de depuración, útil para desarrollo y diagnóstico detallado. |
| **INFO**         | - Configuración de base de datos exitosa<br>- Inicialización de la base de datos<br>- Configuración de CORS<br>- Registro exitoso del blueprint<br>- Creación de tablas<br>- Ejecución del endpoint principal (`/`)<br>- Cantidad de mascotas recuperadas en `/api/debug`<br>- Inicio del entorno Flask (`__main__`) | Registra el flujo normal de ejecución y uso del sistema. Es útil para verificar que el sistema opera correctamente.                       |
| **WARNING**      | - Cuando no hay mascotas registradas en la base de datos (`/api/debug`)                                                                                                                                                                                                                                              | Señala un incidente leve que no detiene la ejecución, pero representa un comportamiento no ideal esperado por el usuario.                 |
| **ERROR**        | - Si falla el registro del blueprint<br>- Si hay errores al crear las tablas<br>- Si ocurre una excepción durante la consulta de mascotas (por conexión o error inesperado)                                                                                                                                          | Captura fallos importantes que afectan la funcionalidad del sistema y necesitan atención inmediata.                                       |

---

### ✅ **Resumen para reporte de práctica**

En el módulo principal `app.py`, el sistema Funkelin implementa los niveles de log para monitorear correctamente las siguientes acciones:

* **DEBUG** rastrea el flujo de configuración, creación de tablas y ejecución de depuración.
* **INFO** documenta la correcta ejecución de procesos clave y uso habitual del sistema.
* **WARNING** alerta de estados anómalos leves, como la ausencia de registros.
* **ERROR** registra problemas críticos, como fallos en el registro de rutas o acceso a base de datos.

Este esquema de logging fortalece la mantenibilidad del sistema, permite una depuración eficiente y da soporte a una operación confiable tanto en desarrollo como en producción.

---


### 🧩 **Aplicación de niveles de logging en el modelo `Mascota`**

| **Nivel de log** | **Ubicación / Acción registrada**                                                                                                                                               | **Justificación**                                                                                                                                         |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **DEBUG**        | - Al iniciar y finalizar `__init__()`<br>- Al ejecutar cada método de validación (`validar_nombre`, `validar_tipo`, `validar_edad`)<br>- Al convertir a diccionario (`to_dict`) | Se rastrea el flujo de ejecución de forma precisa durante la creación y transformación del modelo. Permite seguir paso a paso cómo se procesan los datos. |
| **INFO**         | - Al crear una mascota exitosamente (`Mascota creada exitosamente: {...}`)                                                                                                      | Documenta el uso esperado y correcto del modelo, útil para auditoría de registros exitosos.                                                               |
| **WARNING**      | - Si el nombre, tipo o edad no cumple validaciones básicas                                                                                                                      | Señala incidentes leves como errores de usuario o entradas inválidas sin generar fallos críticos en el sistema.                                           |
| **ERROR**        | - Si ocurre una excepción durante la inicialización del objeto (`ValueError`)                                                                                                   | Captura fallos inesperados que interrumpen la creación del objeto y requieren atención o depuración.                                                      |

---

### ✅ **Resumen para reporte de práctica**

En el modelo `Mascota`, se aplican los niveles de logging según el ciclo de vida del objeto:

* **DEBUG** se usa para rastrear la ejecución desde la validación hasta la conversión del objeto.
* **INFO** documenta instancias creadas exitosamente.
* **WARNING** alerta sobre entradas inválidas antes de lanzar errores.
* **ERROR** registra fallos en la creación de objetos por datos erróneos.

Esta estructura permite monitorear el estado de los objetos del sistema, detectar errores comunes y mejorar la calidad de los datos en tiempo de ejecución.

---

---

### 🧩 **Aplicación de niveles de logging en `routes/mascotas.py`**

| **Nivel de log** | **Ubicación / Acción registrada**                                                                                                                                          | **Justificación**                                                                                                |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **DEBUG**        | - Inicialización del blueprint<br>- Sanitización de texto<br>- Ejecución de funciones clave como `get_mascotas()`, `post_mascota()` y `eliminar_mascota()`                 | Permite rastrear la ejecución detallada y depurar el comportamiento de cada funcionalidad.                       |
| **INFO**         | - Confirmación del funcionamiento del endpoint `/test`<br>- Recuperación exitosa de mascotas<br>- Agregado correcto de una mascota<br>- Eliminación exitosa de una mascota | Registra acciones esperadas realizadas por el usuario en el uso normal del sistema.                              |
| **WARNING**      | - Intento de POST sin datos<br>- Edad no válida en entrada<br>- Fallos de validación del modelo<br>- Intento de eliminar una mascota inexistente                           | Señala incidentes leves que no generan fallos del sistema, pero que deben ser atendidos.                         |
| **ERROR**        | - Excepciones durante la recuperación de mascotas<br>- Fallos al agregar o eliminar mascotas, incluyendo errores de base de datos                                          | Captura eventos que impiden el funcionamiento correcto del sistema, útiles para diagnóstico de errores críticos. |

---

### ✅ **Resumen para reporte de práctica**

En el archivo de rutas `mascotas.py`, correspondiente al blueprint de la API del sistema Funkelin, se han aplicado correctamente los niveles de log propuestos:

* **DEBUG** detalla el flujo de ejecución interno en las rutas, desde la inicialización hasta el manejo de solicitudes.
* **INFO** documenta acciones exitosas llevadas a cabo por los usuarios, como pruebas de conexión, consultas y operaciones CRUD exitosas.
* **WARNING** alerta sobre entradas inválidas o intentos de acción sobre recursos inexistentes, indicando problemas leves que no interrumpen el servicio.
* **ERROR** registra fallos en operaciones críticas como acceso a base de datos o validaciones que no pueden ser satisfechas, permitiendo su posterior análisis.

Esta implementación asegura la trazabilidad completa del comportamiento de la API y mejora tanto el mantenimiento como la capacidad de respuesta ante errores.

---

---

### 🧩 **Aplicación de niveles de logging en `mascota_service.py`**

| **Nivel de log** | **Ubicación / Acción registrada**                                                                                                                                             | **Justificación**                                                                                       |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **DEBUG**        | - Inicio de funciones `agregar_mascota()`, `obtener_mascotas()` y `eliminar_mascota()`<br>- Información detallada sobre los datos de entrada y ejecución de operaciones clave | Facilita el rastreo completo del flujo interno y el análisis de errores en desarrollo o pruebas.        |
| **INFO**         | - Confirmación de que una mascota fue agregada exitosamente<br>- Confirmación de recuperación de lista de mascotas<br>- Confirmación de eliminación exitosa de una mascota    | Documenta que los procesos fundamentales del sistema se realizaron correctamente.                       |
| **WARNING**      | - Validaciones fallidas de entrada en las funciones: nombre, tipo, edad e ID<br>- Intento de eliminar una mascota inexistente                                                 | Avisa sobre condiciones anómalas que no detienen el sistema pero indican un mal uso o riesgo potencial. |
| **ERROR**        | - Fallos en operaciones de base de datos (inserción, consulta, eliminación)<br>- Errores de validación o lógica que impiden la finalización exitosa del proceso               | Captura fallos severos del sistema que requieren atención del desarrollador o administrador.            |

---

### ✅ **Resumen para reporte de práctica**

En el módulo de servicios `mascota_service.py`, se han implementado correctamente los niveles de logging según las mejores prácticas para trazabilidad y tolerancia a fallos:

* **DEBUG** aporta visibilidad detallada del flujo de ejecución y datos de entrada, clave para depuración.
* **INFO** refleja acciones exitosas que son parte del flujo esperado del sistema.
* **WARNING** destaca situaciones prevenibles por el usuario, como datos incorrectos o recursos inexistentes, sin afectar el servicio.
* **ERROR** proporciona trazabilidad sobre errores críticos, incluyendo problemas con SQLAlchemy y validaciones fallidas.

Además, el uso de la librería `retrying` para operaciones con base de datos mejora la **resiliencia del sistema ante fallos transitorios**, y se combina adecuadamente con la gestión de logs para documentar cualquier fallo crítico.

---
