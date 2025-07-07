/************* add_libro,html *************/
const librosTemp = [];

async function buscarLibros(cantidad) {
    try {
        // Convertir a número por si viene como string desde el input
        cantidad = parseInt(cantidad);

        // Validación de entrada
        if (isNaN(cantidad) || cantidad <= 0) {
            cantidad = 10; // Valor por defecto
        }

        if (cantidad > 40) {
            alert('Solo se pueden mostrar hasta 40 resultados.');
            return;
        }

        // Obtener el texto de búsqueda
        const query = document.getElementById('searchInput').value.trim();

        if (query === "") {
            alert("Por favor, ingrese un término de búsqueda.");
            return;
        }

        const url = `https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(query)}&langRestrict=es&maxResults=${cantidad}`;

        // Hacer la solicitud
        const res = await fetch(url);

        if (!res.ok) {
            throw new Error(`Error en la respuesta del servidor: ${res.status}`);
        }

        const data = await res.json();

        if (!data.items || data.items.length === 0) {
            throw new Error("No se encontraron libros.");
        }

        // Mostrar resultados
        mostrarLibros(data.items);
    } catch (error) {
        console.error("Error al buscar libros:", error);
        const container = document.getElementById("resultados");
        container.innerHTML = `<p class="text-danger">Error: ${error.message}</p>`;
    }
}


function mostrarLibros(libros) {
    const container = document.getElementById('resultados');
    container.innerHTML = ''; // Limpiar resultados anteriores
    
    if (!libros || libros.length === 0) {
        container.innerHTML = '<p>No se encontraron libros.</p>';
        return;
    }

    libros.forEach(libro => {
        const info = libro.volumeInfo;
        const title = info.title || "Título desconocido";
        const authors = info.authors ? info.authors.join(', ') : "Autor desconocido";
        const img = info.imageLinks?.thumbnail || 'https://via.placeholder.com/128x180?text=Sin+Portada';

        const libroIndex = librosTemp.push(libro) - 1;

        const card = document.createElement('div');
        card.className = 'col-md-4';

        card.innerHTML = `
            <div class="card h-100">
                <img src="${img}" class="card-img-top" alt="Portada">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${title}</h5>
                    <p class="card-text text-muted">${authors}</p>
                    <button class="btn btn-success mt-auto" onclick="agregarLibro(librosTemp[${libroIndex}])">Agregar</button>
                </div>
            </div>
        `;

        container.appendChild(card);
    });
}

function agregarLibro(libro) {
    const volumeInfo = libro.volumeInfo;
    const accessInfo = libro.accessInfo;

    const datos = {
        titulo: volumeInfo.title || 'Título desconocido',
        subtitulo: volumeInfo.subtitle || '',
        autores: volumeInfo.authors ? volumeInfo.authors.join(', ') : 'Autor desconocido',
        descripcion: volumeInfo.description || '',
        isbn: volumeInfo.industryIdentifiers?.[0]?.identifier || '',
        fecha_publicacion: volumeInfo.publishedDate || '',
        portada: volumeInfo.imageLinks?.thumbnail || 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCySFTjPNnalSUXTEOVkkiPSWJqM6r4_pKjQ&s',
        visibilidad: accessInfo.viewability || 'UNKNOWN', // ALL_PAGES , PARTIAL, NO_PAGES , UNKNOWN
        link_lectura: accessInfo?.webReaderLink || null,
    };

    fetch('/add_libro', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status == 'success') {
            switch (data.accion) {
            case 'nuevo':
                Swal.fire({
                    icon: 'success',
                    title: 'Libro agregado 📚',
                    text: 'Tu libro fue guardado con éxito.'
                });
                break;
            case 'existente_nuevo_usuario':
                Swal.fire({
                    icon: 'success',
                    title: '✅ Ya existía el libro, pero ahora está asociado a vos',
                    text: 'Tu libro fue guardado con éxito.'
                });
                break;
            case 'repetido':
                Swal.fire({
                    icon: 'info',
                    title: 'ℹ️ Ya tenés este libro en tu colección',
                    text: 'El libro ya estaba guardado en tu biblioteca.'
                });
                break;
            }
        }
        else {
            alert('❌ Error al agregar el libro');
        }
        })
    .catch(error => {
        console.error('Error al enviar datos:', error);
    });
}

function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
    let c = cookies[i].trim();
    if (c.startsWith(name + '=')) {
        return c.substring(name.length + 1);
    }
    }
    return '';
}

/************* biblioteca.html *************/

function confirmarEliminacion(event) {
    event.preventDefault();  // detener el envío del formulario

    Swal.fire({
        icon: 'warning',
        title: '¿Estás seguro de que deseas eliminar este libro?',
        text: 'Esta acción no se puede deshacer.',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            event.target.submit();  // si el usuario confirma, enviamos el formulario
        }
    });

    return false; // evitar el envío inmediato del form
}