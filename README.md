 La idea principal del script es permitir a los usuarios activar la geolocalización y encender la cámara directamente desde el navegador web. 🔥

🔧 Características del Script:
- Geolocalización: Captura la ubicación del usuario con el permiso del navegador.
- Cámara: Accede a la cámara para capturar imágenes o transmitir video en tiempo real.
- Flask Backend: Proporciona una estructura eficiente y ligera para manejar las rutas del servidor.

📜 ¿Cómo Funciona?

El backend en Flask sirve una página web donde el usuario otorga permisos de geolocalización y cámara.
Con la ayuda de APIs del navegador (como navigator.geolocation y navigator.mediaDevices.getUserMedia), se activan las funciones para obtener la ubicación y transmitir la cámara.
