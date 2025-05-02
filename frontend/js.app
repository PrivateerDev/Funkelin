// ✅ Obtener referencias del DOM con validaciones
const mascotaForm = document.getElementById("mascotaForm");
const mascotasLista = document.getElementById("mascotasLista");

// ✅ Verificar que los elementos existen antes de usarlos
if (!mascotaForm) throw new Error("⚠ No se encontró el formulario.");
if (!mascotasLista) throw new Error("⚠ No se encontró la lista de mascotas.");

// ✅ Función para obtener mascotas desde el backend con manejo de errores
async function fetchMascotas() {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/mascotas/", {
            method: "GET",
            headers: { "Accept": "application/json" },
            mode: "cors"
        });

        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        const mascotas = await response.json();
        console.assert(Array.isArray(mascotas), "⚠ La respuesta del backend no es una lista válida.");

        mascotasLista.innerHTML = "";

        if (!mascotas.length) {
            mascotasLista.innerHTML = "<li>No hay mascotas registradas.</li>";
        } else {
            mascotas.forEach(mascota => {
                const li = document.createElement("li");
                li.textContent = `${mascota.nombre} (${mascota.tipo}, Edad: ${mascota.edad})`;
                mascotasLista.appendChild(li);
            });
        }
    } catch (error) {
        console.error("⚠ Error al obtener mascotas:", error);
        mascotasLista.innerHTML = "<li>Error al cargar mascotas.</li>";
    }
}

// ✅ Manejo del formulario con validaciones estrictas
mascotaForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const especie = document.getElementById("especie").value.trim();
    const edad = parseInt(document.getElementById("edad").value, 10);

    // ✅ Validaciones de entrada (precondiciones)
    console.assert(typeof nombre === "string" && nombre.length > 1, "⚠ Nombre inválido.");
    console.assert(typeof especie === "string" && especie.length > 1, "⚠ Especie inválida.");
    console.assert(Number.isInteger(edad) && edad > 0, "⚠ Edad inválida.");

    try {
        const response = await fetch("http://127.0.0.1:5000/api/mascotas/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            mode: "cors",
            body: JSON.stringify({ nombre, especie, edad })
        });

        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        console.log("✅ Mascota agregada con éxito");

        // ✅ Postcondición: verificar que los valores se limpiaron correctamente
        document.getElementById("nombre").value = "";
        document.getElementById("especie").value = "";
        document.getElementById("edad").value = "";

        fetchMascotas();
    } catch (error) {
        console.error("⚠ Error al enviar mascota:", error);
    }
});

// ✅ Cargar mascotas al iniciar la página
document.addEventListener("DOMContentLoaded", fetchMascotas);