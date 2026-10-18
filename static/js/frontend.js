// /static/js/frontend.js


document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal');
    const btnNotify = document.getElementById('btnNotifly');
    const closeModal = document.getElementById('closeModal');

    // Abrir modal al hacer clic en las notificaciones
    if (btnNotify && modal) {
        btnNotify.addEventListener('click', () => {
            modal.classList.add('open');
        });
    }

    // Cerrar modal al hacer clic en la (X)
    if (closeModal && modal) {
        closeModal.addEventListener('click', () => {
            modal.classList.remove('open');
        });
    }

    // Opcional: Cerrar modal si se hace clic fuera del contenido
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('open');
        }
    });
});

const eventSource = new EventSource('/api/v1/event/web');

eventSource.onmessage = (event) => {
    try { 
        const data = JSON.parse(event.data); 
        const idDispositivo = data.device_id;
        const usuario = data.username;
        const empresa = data.empresa;
        const version_android = data.version_android;

        console.log(`[+] dato recibido correctamente: ${usuario}`);
        // console.log(data)

        datapop(idDispositivo, usuario, empresa, version_android);
        

    } catch (e) {
        console.error("[-] Error en recepción de datos", e);
    }
};

function datapop(idDispositivo, usuario, empresa, version_android) {
    const tbody = document.querySelector('.modal-table tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    const tr = document.createElement('tr');
    tr.id = `card-${idDispositivo}`;

    // Estructura HTML corregida (sin anidación de <td> duplicada y con sintaxis onclick válida)
    tr.innerHTML = `
        <td>${idDispositivo}</td>
        <td>${usuario}</td>
        <td>${empresa}</td>
        <td>${version_android}</td>
        <td class="action-buttons">
            <button type="button" class="btn-accept" onclick="ejecutarRespuesta(event, '${idDispositivo}', 'approved')">Aceptar</button>
            <button type="button" class="btn-reject" onclick="ejecutarRespuesta(event, '${idDispositivo}', 'blocked')">Rechazar</button>
        </td>
    `;

    tbody.appendChild(tr);
}

// Wrapper para evitar la recarga por defecto si los botones están dentro de un <form>
function ejecutarRespuesta(event, deviceId, status) {
    if (event) event.preventDefault(); // Previene la cancelación de la solicitud por navegación
    responderSolicitud(deviceId, status);
}

async function responderSolicitud(deviceId, status) {
    try {
        const respuesta = await fetch('/api/v1/event/app', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify({ 
                device_id: deviceId, 
                status: status 
            })
        });

        if (respuesta.ok) {
            const tarjeta = document.getElementById(`card-${deviceId}`);
            if (tarjeta) tarjeta.remove();
        } else {
            console.error("Error en la respuesta del servidor:", respuesta.status);
        }
    } catch (error) {
        console.error("Error al enviar la solicitud:", error);
    }
}

eventSource.onerror = (error) => {
    console.error("Error en la conexión SSE:", error);
};