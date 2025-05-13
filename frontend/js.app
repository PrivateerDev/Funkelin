// ✅ Obtener referencias del DOM con validaciones
const mascotaForm = document.getElementById("mascotaForm");
const mascotasLista = document.getElementById("mascotasLista");

console.debug("📡 Inicializando referencias del DOM...");

// ✅ Verificar que los elementos existen antes de usarlos
if (!mascotaForm) {
    console.error("⚠ No se encontró el formulario.");
    throw new Error("⚠ No se encontró el formulario.");
}
if (!mascotasLista) {
    console.error("⚠ No se encontró la lista de mascotas.");
    throw new Error("⚠ No se encontró la lista de mascotas.");
}

// ✅ Función para obtener mascotas desde el backend con manejo de errores
async function fetchMascotas() {
    console.debug("📡 Ejecutando `fetchMascotas()`...");

    try {
        console.info("📡 Solicitando lista de mascotas al backend...");
        const response = await fetch("http://127.0.0.1:5000/api/mascotas/", {
            method: "GET",
            headers: { "Accept": "application/json" },
            mode: "cors"
        });

        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        const mascotas = await response.json();
        console.assert(Array.isArray(mascotas), "⚠ La respuesta del backend no es una lista válida.");

        console.info(`✅ Se recibieron ${mascotas.length} mascotas.`);
        mascotasLista.innerHTML = mascotas.length ? "" : "<li>No hay mascotas registradas.</li>";
        mascotas.forEach(mascota => agregarMascotaDOM(mascota));

    } catch (error) {
        console.error("⚠ Error al obtener mascotas:", error);
        mascotasLista.innerHTML = "<li>Error al cargar mascotas.</li>";
    }
}

// ✅ Manejo del formulario con validaciones estrictas
mascotaForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    let nombre = document.getElementById("nombre").value.trim();
    let especie = document.getElementById("especie").value.trim();
    let edad = parseInt(document.getElementById("edad").value, 10);

    console.info("📡 Enviando datos al backend:", { nombre, especie, edad });

    // ✅ Validaciones de entrada (precondiciones)
    if (!nombre || nombre.length < 2 || nombre.length > 50) {
        console.warn("⚠ Nombre inválido:", nombre);
        return alert("El nombre debe tener entre 2 y 50 caracteres.");
    }
    if (!especie) {
        console.warn("⚠ Especie inválida:", especie);
        return alert("Debes seleccionar un tipo válido.");
    }
    if (!Number.isInteger(edad) || edad <= 0) {
        console.warn("⚠ Edad inválida:", edad);
        return alert("La edad debe ser un número entero positivo.");
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/api/mascotas/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            mode: "cors",
            body: JSON.stringify({ nombre, especie, edad })
        });

        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        console.info("✅ Mascota agregada con éxito");

        // ✅ Postcondición: verificar que los valores se limpiaron correctamente
        document.getElementById("nombre").value = "";
        document.getElementById("especie").value = "";
        document.getElementById("edad").value = "";

        fetchMascotas();
    } catch (error) {
        console.error("⚠ Error al enviar mascota:", error);
    }
});

// ✅ Función para agregar una mascota al DOM con validación segura
function agregarMascotaDOM(mascota) {
    console.debug("📡 Agregando mascota al DOM:", mascota);

    if (!mascota?.id) {
        console.warn("⚠ ID de mascota inválido:", mascota);
        return;
    }

    const li = document.createElement("li");
    li.textContent = `${mascota.nombre} (${mascota.tipo ?? "Desconocida"}, Edad: ${mascota.edad})`;

    mascotasLista.appendChild(li);
}

// ✅ Cargar mascotas al iniciar la página
document.addEventListener("DOMContentLoaded", () => {
    console.debug("📡 Cargando mascotas al iniciar la página...");
    fetchMascotas();
});