// frontend/script.js
export async function fetchMascotas() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/mascotas');
        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        return await response.json();
    } catch (error) {
        console.error('Error al obtener mascotas:', error);
        return [];
    }
}// Archivo JavaScript para Funkelin
