// Seleccionar elementos del DOM
const mascotaForm = document.getElementById('mascotaForm');
const mascotasLista = document.getElementById('mascotasLista');

// Función para obtener la lista de mascotas desde el backend
async function fetchMascotas() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/mascotas');
        const mascotas = await response.json();
        mascotasLista.innerHTML = '';
        mascotas.forEach(mascota => {
            const li = document.createElement('li');
            li.textContent = `${mascota.nombre} (${mascota.tipo}, Edad: ${mascota.edad})`; // Mostrar "tipo" en lugar de "especie"
            mascotasLista.appendChild(li);
        });
    } catch (error) {
        console.error('Error al obtener mascotas:', error);
    }
}
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
    } catch (error) {
        console.error('Error al enviar mascota:', error);
    }
});

// Cargar la lista de mascotas al iniciar
fetchMascotas();