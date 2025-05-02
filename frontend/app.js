// ✅ Obtener referencias del DOM con validaciones
const mascotaForm = document.getElementById("mascotaForm");
const mascotasLista = document.getElementById("mascotasLista");

// ✅ Verificar que los elementos existen antes de usarlos
if (!mascotaForm) throw new Error("⚠ No se encontró el formulario.");
if (!mascotasLista) throw new Error("⚠ No se encontró la lista de mascotas.");

// ✅ Función para sanitizar texto de entrada
function sanitizarTexto(texto) {
    return texto.replace(/[<>\"\'&]/g, "").trim();
}

// ✅ Función para obtener mascotas desde el backend con manejo de errores
async function fetchMascotas() {
    try {
        console.log("📡 Obteniendo lista de mascotas...");
        const response = await fetch("http://127.0.0.1:5000/api/mascotas/", {
            method: "GET",
            headers: { "Accept": "application/json" }
        });

        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        const mascotas = await response.json();
        console.assert(Array.isArray(mascotas), "⚠ La respuesta del backend no es una lista válida.");

        console.log("📡 Mascotas recibidas:", mascotas);

        // ✅ Limpiar lista sin borrar completamente
        mascotasLista.innerHTML = mascotas.length ? "" : "<li>No hay mascotas registradas.</li>";

        mascotas.forEach(mascota => agregarMascotaDOM(mascota));
    } catch (error) {
        console.error("⚠ Error al obtener mascotas:", error);
        mascotasLista.innerHTML = "<li>Error al cargar mascotas.</li>";
    }
}

// ✅ Función para agregar una mascota al DOM con validación de ID
function agregarMascotaDOM(mascota) {
    if (!mascota.id) {
        console.error("⚠ ID de mascota inválido:", mascota);
        return;
    }

    const li = document.createElement("li");
    li.textContent = `${mascota.nombre} (${mascota.especie ?? "Desconocida"}, Edad: ${mascota.edad})`;

    // ✅ Botón de eliminación con ID asignado correctamente
    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Eliminar";
    deleteBtn.className = "delete-btn";
    deleteBtn.setAttribute("data-id", mascota.id);
    deleteBtn.onclick = function() {
        eliminarMascota(this.getAttribute("data-id"));
    };

    li.appendChild(deleteBtn);
    mascotasLista.appendChild(li);
}

// ✅ Manejo del formulario con validaciones estrictas y actualización en tiempo real
mascotaForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    let nombre = sanitizarTexto(document.getElementById("nombre").value);
    let especie = document.getElementById("especie").value;
    let edad = parseInt(document.getElementById("edad").value, 10);

    console.log("📡 Enviando datos:", { nombre, especie, edad });

    // ✅ Validaciones de entrada
    if (!nombre || nombre.length < 2 || nombre.length > 50) {
        alert("⚠ El nombre debe tener entre 2 y 50 caracteres.");
        return;
    }
    if (!especie) {
        alert("⚠ Debes seleccionar una especie válida.");
        return;
    }
    if (!Number.isInteger(edad) || edad <= 0) {
        alert("⚠ La edad debe ser un número entero positivo.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/api/mascotas/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, especie, edad })
        });

        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        console.log("✅ Mascota agregada con éxito");

        // ✅ Obtiene la mascota con su ID desde el backend y la agrega al DOM
        const nuevaMascota = await response.json();
        agregarMascotaDOM(nuevaMascota);

        // ✅ Limpiar el formulario
        mascotaForm.reset();
    } catch (error) {
        console.error("⚠ Error al enviar mascota:", error);
    }
});

// ✅ Función para eliminar una mascota con validación de ID
async function eliminarMascota(id) {
    if (!id || isNaN(id)) {
        console.error("⚠ ID de mascota inválido:", id);
        return;
    }

    try {
        console.log(`📡 Eliminando mascota con ID: ${id}`);
        const response = await fetch(`http://127.0.0.1:5000/api/mascotas/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        console.log(`✅ Mascota con ID ${id} eliminada correctamente`);
        fetchMascotas(); // ✅ Refrescar la lista sin recargar la página
    } catch (error) {
        console.error("⚠ Error al eliminar mascota:", error);
    }
}

// ✅ Cargar mascotas al iniciar la página
document.addEventListener("DOMContentLoaded", fetchMascotas);
