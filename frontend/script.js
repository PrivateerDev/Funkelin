// ✅ Función para obtener mascotas con validaciones avanzadas
export async function fetchMascotas() {
    try {
        console.log("🔎 Iniciando solicitud para obtener mascotas...");

        const response = await fetch("http://127.0.0.1:5000/api/mascotas", {
            method: "GET",
            headers: { "Accept": "application/json" },
            mode: "cors"
        });

        // ✅ Validar respuesta HTTP antes de procesar datos
        console.assert(response instanceof Response, "⚠ La respuesta no es un objeto Response.");
        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        const mascotas = await response.json();

        // ✅ Postcondición: Verificar que los datos recibidos son correctos
        console.assert(Array.isArray(mascotas), "⚠ La respuesta del backend no es una lista válida.");
        console.assert(mascotas.every(m => typeof m.nombre === "string"), "⚠ Alguna mascota no tiene un nombre válido.");

        console.log("✅ Mascotas obtenidas con éxito:", mascotas);

        return mascotas;

    } catch (error) {
        console.error("⚠ Error al obtener mascotas:", error);
        return [];
    }
}
