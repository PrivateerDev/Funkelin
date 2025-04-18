<<<<<<< HEAD
// ✅ Obtener referencias del DOM con validaciones mejoradas
const mascotaForm = document.getElementById("mascotaForm");
const mascotasLista = document.getElementById("mascotasLista");

if (!mascotaForm || !mascotasLista) {
    console.error("⚠ Elementos críticos no encontrados en el DOM.");
    alert("Error de inicialización: Verifica que la página cargó correctamente.");
}

// ✅ Función para sanitizar texto de entrada y prevenir ataques XSS
function sanitizarTexto(texto) {
    console.debug(`Sanitizando texto: ${texto}`);
    return texto.replace(/[<>\"'&]/g, "").trim();
}

// ✅ Función para obtener mascotas con manejo seguro de errores
=======
// Seleccionar elementos del DOM
const mascotaForm = document.getElementById('mascotaForm');
const mascotasLista = document.getElementById('mascotasLista');

// Función para obtener la lista de mascotas desde el backend
>>>>>>> f978f38 (Reinstanciación completa del backend:)
async function fetchMascotas() {
    console.debug("📡 Ejecutando `fetchMascotas()` para obtener mascotas...");

    try {
<<<<<<< HEAD
        console.info("📡 Solicitando lista de mascotas al backend...");
        const response = await fetch("http://127.0.0.1:5000/api/mascotas/", {
            method: "GET",
            headers: { "Accept": "application/json" }
=======
        const response = await fetch('http://127.0.0.1:5000/api/mascotas');
        const mascotas = await response.json();
        mascotasLista.innerHTML = '';
        mascotas.forEach(mascota => {
            const li = document.createElement('li');
            li.textContent = `${mascota.nombre} (${mascota.tipo}, Edad: ${mascota.edad})`; // Mostrar "tipo" en lugar de "especie"
            mascotasLista.appendChild(li);
>>>>>>> f978f38 (Reinstanciación completa del backend:)
        });

        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        const mascotas = await response.json();
        if (!Array.isArray(mascotas)) throw new Error("⚠ La respuesta del backend no es válida.");

        console.info(`✅ Se recibieron ${mascotas.length} mascotas.`);
        mascotasLista.innerHTML = mascotas.length ? "" : "<li>No hay mascotas registradas.</li>";
        mascotas.forEach(mascota => agregarMascotaDOM(mascota));

    } catch (error) {
        console.error("⚠ Error al obtener mascotas:", error);
        mascotasLista.innerHTML = "<li>Error al cargar mascotas.</li>";
    }
}
<<<<<<< HEAD

// ✅ Función para agregar una mascota al DOM con validación segura
function agregarMascotaDOM(mascota) {
    console.debug("📡 Agregando mascota al DOM:", mascota);

    if (!mascota?.id) {
        console.warn("⚠ ID de mascota inválido:", mascota);
        return;
    }

    const li = document.createElement("li");
    li.textContent = `${mascota.nombre} (${mascota.tipo ?? "Desconocida"}, Edad: ${mascota.edad})`;

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Eliminar";
    deleteBtn.className = "delete-btn";
    deleteBtn.setAttribute("data-id", mascota.id);
    deleteBtn.onclick = () => eliminarMascota(mascota.id);

    li.appendChild(deleteBtn);
    mascotasLista.appendChild(li);
}

// ✅ Exponer funciones al contexto global para pruebas en consola
window.agregarMascotaDOM = agregarMascotaDOM;
window.fetchMascotas = fetchMascotas;
window.eliminarMascota = eliminarMascota;

// ✅ Manejo del formulario con validaciones estrictas y actualización segura
mascotaForm?.addEventListener("submit", async (event) => {
    event.preventDefault();

    let nombre = sanitizarTexto(document.getElementById("nombre")?.value);
    let tipo = document.getElementById("especie")?.value;
    let edad = parseInt(document.getElementById("edad")?.value, 10);

    console.info("📡 Enviando datos al backend:", { nombre, tipo, edad });

    // ✅ Validaciones de entrada reforzadas
    if (!nombre || nombre.length < 2 || nombre.length > 50) return alert("⚠ El nombre debe tener entre 2 y 50 caracteres.");
    if (!tipo) return alert("⚠ Debes seleccionar un tipo válido.");
    if (!Number.isInteger(edad) || edad <= 0) return alert("⚠ La edad debe ser un número entero positivo.");

    try {
        const response = await fetch("http://127.0.0.1:5000/api/mascotas/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, tipo, edad })
        });

        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        const nuevaMascota = await response.json();
        agregarMascotaDOM(nuevaMascota);

        fetchMascotas();  // ✅ Refrescar lista después de agregar mascota

        mascotaForm.reset();

        console.info("✅ Mascota agregada con éxito y lista actualizada.");
=======
// Manejar el evento de envío del formulario
mascotaForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevenir que la página se recargue
    const nombre = document.getElementById('nombre').value;
    const especie = document.getElementById('especie').value;
    const edad = document.getElementById('edad').value; // Nuevo campo para la edad

    try {
        const response = await fetch('http://127.0.0.1:5000/api/mascotas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre, especie, edad }) // Incluir edad en el cuerpo del POST
        });
        if (response.ok) {
            document.getElementById('nombre').value = ''; // Limpiar el formulario
            document.getElementById('especie').value = '';
            document.getElementById('edad').value = ''; // Limpiar el campo de edad
            fetchMascotas(); // Actualizar la lista de mascotas
        } else {
            console.error('Error al agregar mascota');
        }
>>>>>>> f978f38 (Reinstanciación completa del backend:)
    } catch (error) {
        console.error("⚠ Error al enviar mascota:", error);
    }
});

// ✅ Función para eliminar una mascota con validación de ID y manejo estructurado de errores
async function eliminarMascota(id) {
    console.debug(`📡 Ejecutando eliminarMascota() con ID: ${id}`);

    if (!id || isNaN(id)) {
        console.warn("⚠ ID de mascota inválido:", id);
        return;
    }

    try {
        console.info(`📡 Eliminando mascota con ID: ${id}`);
        const response = await fetch(`http://127.0.0.1:5000/api/mascotas/${id}`, { method: "DELETE" });

        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        console.info(`✅ Mascota con ID ${id} eliminada correctamente`);
        fetchMascotas();  // ✅ Actualizar lista sin recargar la página
    } catch (error) {
        console.error("⚠ Error al eliminar mascota:", error);
    }
}

// ✅ Cargar mascotas al iniciar la página con validación de carga
document.addEventListener("DOMContentLoaded", () => {
    console.debug("📡 Cargando mascotas al iniciar la página...");
    if (mascotasLista) fetchMascotas();
});