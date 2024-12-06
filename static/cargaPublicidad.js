    
        const videoInput = document.getElementById('template-input');
        const videoPreviewContainer = document.getElementById('video-preview-container');
        const videoPreview = document.getElementById('video-preview');
        const dragArea = document.getElementById('drag-area');
        const uploadButtons = document.getElementById("upload-buttons");
        const loadingText = document.getElementById("loading-text");

        // Manejo de drag and drop para evitar abrir en una pestaña nueva
        dragArea.addEventListener('dragover', (event) => {
            event.preventDefault();
            dragArea.classList.add('dragover');
        });

        dragArea.addEventListener('dragleave', () => {
            dragArea.classList.remove('dragover');
        });

        dragArea.addEventListener('drop', (event) => {
            event.preventDefault();
            dragArea.classList.remove('dragover');
            const file = event.dataTransfer.files[0];
            if (file && file.type.startsWith('video/')) {
                handleVideoPreview(file);
            }
        });

        // Previsualización del video cuando se selecciona o se hace drag & drop
        videoInput.addEventListener('change', function () {
            const file = videoInput.files[0];
            if (file) {
                handleVideoPreview(file);
            }
        });

        // Manejo de la previsualización y mostrar botones de enviar
        function handleVideoPreview(file) {
            const fileURL = URL.createObjectURL(file);
            videoPreview.src = fileURL;
            videoPreviewContainer.classList.remove('hidden');
            uploadButtons.classList.remove('hidden');
        }

        // Eliminar video cargado
        function removeVideo() {
            videoInput.value = '';
            videoPreview.src = '';
            videoPreviewContainer.classList.add('hidden');
            uploadButtons.classList.add('hidden');
        }

        // Función para manejar el envío del formulario
        function handleFormSubmit(event) {
            event.preventDefault();

            // Ocultar botones y mostrar loading
            uploadButtons.classList.add("hidden");
            loadingText.classList.remove("hidden");

            // Subir el archivo al servidor
            const formData = new FormData(event.target);
            fetch(event.target.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(() => {
                // Iniciar el proceso de conversión FFMPEG automáticamente
                uploadStart();
            })
            .catch(error => {
                alert("Error: " + error.message);
                resetForm();
            });
        }

        // Función para resetear el formulario en caso de error
        function resetForm() {
            uploadButtons.classList.remove("hidden");
            loadingText.classList.add("hidden");
        }

        // Función para iniciar el proceso de conversión de FFMPEG
        async function uploadStart() {
            let file = document.getElementById("template-input");
            if (file.files.length === 0) {
                alert("No file selected");
                return;
            }
            let fileName = file.files[0].name;
            fetch(`http://${SERVER_IP}:${SERVER_PORT}/publicidad/start/`, {
                method: "POST",
                body: JSON.stringify({
                    command: "ffmpeg -i ./publicidad/".concat(fileName, " -c:v libx264 ./publicidad/", fileName.substring(0, fileName.lastIndexOf('.')), ".m3u8")
                }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
            })
            .then(data => {
                alert("Video processed successfully!");
            })
            .catch(error => {
                alert("Error: " + error.message);
                console.log(error);
            });
        }

        // Monitorear el estado del procesamiento de FFMPEG
        setInterval(() => {
            fetch(`http://${SERVER_IP}:${SERVER_PORT}/publicidad/status/`)
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('API request failed');
                    }
                })
                .then(data => {
                    document.getElementById("ffmpeg-text").textContent = data["text"];
                })
                .catch(error => {
                    console.error(error);
                });

        }, 50);