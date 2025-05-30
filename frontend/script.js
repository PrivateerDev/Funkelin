// ✅ Función para obtener mascotas con validaciones avanzadas y manejo resiliente
export async function fetchMascotas() {
    console.debug("📡 Ejecutando fetchMascotas() para obtener mascotas...");

    const CONTROLLER = new AbortController();  // ✅ Agregar un timeout para evitar bloqueos
    const TIMEOUT_MS = 5000; // ⏳ Tiempo máximo de espera
    const timeoutId = setTimeout(() => {
        CONTROLLER.abort();
        console.warn("⏳ Solicitud abortada: tiempo de espera excedido.");
    }, TIMEOUT_MS);

    try {
        console.info("🔎 Iniciando solicitud al backend...");

        const response = await fetch("http://127.0.0.1:5000/api/mascotas", {
            method: "GET",
            headers: { "Accept": "application/json" },
            mode: "cors",
            signal: CONTROLLER.signal  // ✅ Asociar el timeout
        });

        clearTimeout(timeoutId); // ✅ Limpiar el timeout correctamente

        // ✅ Validar respuesta HTTP antes de procesar datos
        if (!response.ok) throw new Error(Error ${response.status}: ${response.statusText});

        const mascotas = await response.json();

        // ✅ Validar estructura del JSON antes de continuar
        if (!Array.isArray(mascotas)) throw new Error("⚠ La respuesta del backend no es una lista válida.");
        if (!mascotas.every(m => typeof m.nombre === "string")) throw new Error("⚠ Alguna mascota no tiene un nombre válido.");

        console.info(✅ Mascotas obtenidas con éxito (${mascotas.length} registros));
        return mascotas;

    } catch (error) {
        clearTimeout(timeoutId); // ✅ Asegurar que el timeout siempre se limpia

        if (error.name === "AbortError") {
            console.error("⏳ Tiempo de espera excedido al obtener mascotas.");
        } else {
            console.error("⚠ Error al obtener mascotas:", error);
        }
        return [];
    }
}