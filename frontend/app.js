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
async function fetchMascotas() {
    console.debug("📡 Ejecutando `fetchMascotas()` para obtener mascotas...");

    try {
        console.info("📡 Solicitando lista de mascotas al backend...");
        const response = await fetch("http://127.0.0.1:5000/api/mascotas/", {
            method: "GET",
            headers: { "Accept": "application/json" }
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