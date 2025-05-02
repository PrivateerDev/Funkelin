// ✅ Función para obtener mascotas con validaciones avanzadas y manejo resiliente
export async function fetchMascotas() {
    const CONTROLLER = new AbortController();  // ✅ Agregar un timeout para evitar bloqueos
    const TIMEOUT_MS = 5000; // ⏳ Tiempo máximo de espera

    try {
        console.log("🔎 Iniciando solicitud para obtener mascotas...");
        
        // ✅ Configurar timeout en la solicitud
        const timeout = setTimeout(() => CONTROLLER.abort(), TIMEOUT_MS);

        const response = await fetch("http://127.0.0.1:5000/api/mascotas", {
            method: "GET",
            headers: { "Accept": "application/json" },
            mode: "cors",
            signal: CONTROLLER.signal // ✅ Asociar el timeout
        });

        clearTimeout(timeout); // ✅ Limpiar timeout si la solicitud se completa

        // ✅ Validar respuesta HTTP antes de procesar datos
        console.assert(response instanceof Response, "⚠ La respuesta no es un objeto Response.");
        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        const mascotas = await response.json();

        // ✅ Postcondición: Verificar que los datos recibidos son correctos
        if (!Array.isArray(mascotas)) throw new Error("⚠ La respuesta del backend no es una lista válida.");
        if (!mascotas.every(m => typeof m.nombre === "string")) throw new Error("⚠ Alguna mascota no tiene un nombre válido.");

        console.log("✅ Mascotas obtenidas con éxito:", mascotas);

        return mascotas;

    } catch (error) {
        if (error.name === "AbortError") {
            console.error("⏳ Tiempo de espera excedido al obtener mascotas.");
        } else {
            console.error("⚠ Error al obtener mascotas:", error);
        }
        return [];
    }
}