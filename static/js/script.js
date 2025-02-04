const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const preview = document.getElementById('preview');

// Función para capturar la imagen automáticamente
function capturePhoto() {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convertir la imagen a base64
    const imageData = canvas.toDataURL('image/png');
    preview.src = imageData;

    // Enviar la imagen al servidor automáticamente
    enviarImagen(imageData);

    // Detener la cámara
    const stream = video.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach(track => track.stop());
    video.style.display = 'none';  // Ocultar el video después de capturar la imagen
}

// Función para enviar la imagen al servidor
function enviarImagen(imageData) {
    const formData = new FormData();
    formData.append('imageData', imageData);

    fetch('/devolucion', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Devolución enviada:', data.message);
    })
    .catch(error => {
        console.error('Error al enviar la imagen:', error);
    });
}

// Acceder a la cámara y capturar la imagen automáticamente
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;

        // Capturar la imagen automáticamente después de 2 segundos
        setTimeout(() => {
            capturePhoto();
        }, 2000);
    })
    .catch(error => {
        console.error('Error accediendo a la cámara:', error);
    });