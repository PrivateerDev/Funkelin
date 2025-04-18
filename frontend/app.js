const mascotaForm = document.getElementById('mascotaForm');
const mascotasLista = document.getElementById('mascotasLista');

// Función para obtener la lista de mascotas
async function fetchMascotas() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/mascotas');
        const mascotas = await response.json();
        mascotasLista.innerHTML = '';
        mascotas.forEach(mascota => {
            const li = document.createElement('li');
            li.textContent = `${mascota.nombre} (${mascota.especie})`;
            mascotasLista.appendChild(li);
        });
    } catch (error) {
        console.error('Error al obtener mascotas:', error);
    }
}

// Manejar el formulario para agregar mascotas
mascotaForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const nombre = document.getElementById('nombre').value;
    const especie = document.getElementById('especie').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/api/mascotas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre, especie })
        });
        if (response.ok) {
            document.getElementById('nombre').value = '';
            document.getElementById('especie').value = '';
            fetchMascotas(); // Actualizar la lista
        } else {
            console.error('Error al agregar mascota');
        }
    } catch (error) {
        console.error('Error al enviar mascota:', error);
    }
});

// Cargar la lista de mascotas al iniciar
fetchMascotas();