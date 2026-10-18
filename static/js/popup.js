// frontend.js

const eventSource = new EventSource('https://unalignable-semiexperimentally-olive.ngrok-free.dev/api/v1/event/web'); // o la URL completa de tu backend FastAPI

// Escuchar mensajes entrantes
eventSource.onmessage = (event) => {
    try {
        const data = JSON.parse(event.data);
        console.log("Notificación recibida en tiempo real:", data);
        
        // Aquí actualizas tu UI / Dashboard con la nueva solicitud de dispositivo
        alert(`Nueva solicitud del dispositivo: ${data.device_id}`);
    } catch (e) {
        console.log("Mensaje recibido (texto plano):", event.data);
    }
};

eventSource.onerror = (error) => {
    console.error("Error en la conexión SSE:", error);
    // EventSource reconectará automáticamente si la conexión se cae
};

