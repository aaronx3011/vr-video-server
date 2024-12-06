// Función para manejar la subida de múltiples imágenes
async function handleFormSubmit(event) {
    event.preventDefault();

    const fileInput = document.getElementById("template-input");
    const formData = new FormData(event.target);

    if (fileInput.files.length === 0) {
        alert("No images selected for upload");
        return;
    }

    // Mostrar texto de carga
    document.getElementById("upload-buttons").classList.add("hidden");
    document.getElementById("loading-text").classList.remove("hidden");

    // Subir las imágenes al servidor local
    fetch(event.target.action, {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(() => {
        fetch(`http://${SERVER_IP}:${SERVER_PORT}/bucket/sync/folder/`,
            {
                method: "POST",
                body: JSON.stringify(
                    {folderName: "banners"}
                ),
                headers: {
                "Content-type": "application/json; charset=UTF-8",
                },
            }
        )
        .then(response => {
            if (response.ok) {
                alert("Banners uploaded succesfully");
                return response.json();
            } else {
                throw new Error('API request failed');
            }
        })
        document.getElementById("loading-text").classList.add("hidden");
    })
    .catch(error => {
        alert("Error during upload: " + error.message);
        console.error(error);
        document.getElementById("loading-text").classList.add("hidden");
        document.getElementById("upload-buttons").classList.remove("hidden");
    });
}

// Previsualización de múltiples imágenes seleccionadas
document.getElementById("template-input").addEventListener("change", function () {
    const files = Array.from(this.files); // Convertir a un arreglo para mantener las imágenes previas
    const imagePreviewContainer = document.getElementById("image-preview-container");

    // Asegurarse de que no se sobreescriban las imágenes previas
    imagePreviewContainer.innerHTML = '';

    if (files.length > 0) {
        files.forEach((file, index) => {
            if (file.type.startsWith("image/")) {
                const fileURL = URL.createObjectURL(file);

                // Crear contenedor para la imagen y el botón de eliminación
                const imageContainer = document.createElement("div");
                imageContainer.classList.add("relative", "flex", "items-center", "justify-center");

                const image = document.createElement("img");
                image.src = fileURL;
                image.classList.add("w-full", "rounded-lg","object-cover");

                // Botón de eliminación
                const removeButton = document.createElement("button");
                removeButton.innerText = "✖";
                removeButton.classList.add("absolute", "top-0", "right-0", "bg-red-500", "text-white", "text-xs", "rounded-full", "p-1", "hover:bg-red-600");
                removeButton.setAttribute("data-index", index);
                removeButton.onclick = function () {
                    removeImage(index);
                };

                // Agregar imagen y botón de eliminación al contenedor
                imageContainer.appendChild(image);
                imageContainer.appendChild(removeButton);

                // Agregar contenedor al área de previsualización
                imagePreviewContainer.appendChild(imageContainer);
            }
        });

        // Mostrar contenedor de previsualización y botones
        document.getElementById("image-preview-container").classList.remove("hidden");
        document.getElementById("upload-buttons").classList.remove("hidden");
    }
});

// Función para eliminar una imagen individual por su índice
function removeImage(index) {
    const fileInput = document.getElementById("template-input");
    const files = Array.from(fileInput.files);

    // Remover el archivo seleccionado
    files.splice(index, 1);

    // Crear un nuevo objeto FileList
    const newFileList = new DataTransfer();
    files.forEach(file => {
        newFileList.items.add(file);
    });

    fileInput.files = newFileList.files;

    // Actualizar la previsualización
    const event = new Event('change');
    fileInput.dispatchEvent(event);
}

// Monitorear el estado del procesamiento en AWS (opcional)
setInterval(() => {
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/resources/process/aws/status/`)
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
}, 5000); // Cada 5 segundos
