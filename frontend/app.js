// ✅ Obtener referencias del DOM
const mascotaForm = document.getElementById("mascotaForm");
const mascotasLista = document.getElementById("mascotasLista");

// ✅ Verificar que los elementos existen antes de usarlos
if (!mascotaForm) console.error("⚠ No se encontró el formulario.");
if (!mascotasLista) console.error("⚠ No se encontró la lista de mascotas.");

// ✅ Función para obtener mascotas desde el backend
async function fetchMascotas() {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/mascotas/", {
            method: "GET",
            headers: { "Accept": "application/json" },
            mode: "cors" // ✅ Solución al bloqueo de CORS
        });

        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        const mascotas = await response.json();
        console.log("🔎 Mascotas obtenidas:", mascotas); // ✅ Verificación en consola

        mascotasLista.innerHTML = ""; // ✅ Limpiar la lista antes de actualizar

        if (!mascotas.length) {
            mascotasLista.innerHTML = "<li>No hay mascotas registradas.</li>"; // ✅ Mensaje si la lista está vacía
        } else {
            mascotas.forEach(mascota => {
                const li = document.createElement("li");
                li.textContent = `${mascota.nombre} (${mascota.tipo}, Edad: ${mascota.edad})`;
                mascotasLista.appendChild(li);
            });
        }
    } catch (error) {
        console.error("⚠ Error al obtener mascotas:", error);
        mascotasLista.innerHTML = "<li>Error al cargar mascotas</li>";
    }
}

// ✅ Manejo del formulario para agregar mascotas
mascotaForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const especie = document.getElementById("especie").value.trim();
    const edad = parseInt(document.getElementById("edad").value, 10);

    // ✅ Validar datos antes de enviarlos
    if (!nombre || !especie || isNaN(edad) || edad <= 0) {
        console.error("⚠ Datos inválidos para agregar mascota.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/api/mascotas/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            mode: "cors", // ✅ Solución al bloqueo de CORS
            body: JSON.stringify({ nombre, especie, edad })
        });

        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        console.log("✅ Mascota agregada con éxito");

        // ✅ Limpiar el formulario después de agregar la mascota
        document.getElementById("nombre").value = "";
        document.getElementById("especie").value = "";
        document.getElementById("edad").value = "";

        fetchMascotas(); // ✅ Refrescar la lista después de agregar mascota
    } catch (error) {
        console.error("⚠ Error al enviar mascota:", error);
    }
});

// ✅ Cargar mascotas al iniciar la página
fetchMascotas();
