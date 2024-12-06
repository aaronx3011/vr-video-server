function clearOption() {
  console.log("clear");
  let selects = document.getElementsByClassName("test-select");
  console.log(selects);
  for (let i = 0; i < selects.length; i++) {
    console.log(selects[i].childElementCount);
  }
}

function addOption(className, text, value) {
  let selects = document.getElementsByClassName(className);
  for (let i = 0; i < selects.length; i++) {
    let newOption = new Option(text, value);
    selects[i].appendChild(newOption);
  }
}

function getDirectoriesInDirectory() {
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/bucket/list/directories/`,
    {
        method: "POST",
        body: JSON.stringify(
            {
                directory: "transmision/high/"
            }
        ),
        headers: {
        "Content-type": "application/json; charset=UTF-8",
        },
    }
    ).then((response) => {
        if (response.ok) {
        return response.json();
        } else {
        throw new Error("API request failed");
        }
    })
    .then((data) => {
        console.log(data);
        clearOption();
        for (i in data) {
            console.log(data[i]);
            addOption("directories-dropdown", data[i],data[i]);
        }
        }
    );
}

function getObjectsInDirectory() {
    let streamName = document.getElementById("directories-dropdown");
    console.log(streamName.options[streamName.selectedIndex].text.split('.').slice(0, -1).join('.') + "high/")
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/bucket/list/playlists/`,
    {
        method: "POST",
        body: JSON.stringify(
            {
                directory: streamName.options[streamName.selectedIndex].text + "high/"
            }
        ),
        headers: {
        "Content-type": "application/json; charset=UTF-8",
        },
    }
    ).then((response) => {
        if (response.ok) {
        return response.json();
        } else {
        throw new Error("API request failed");
        }
    })
    .then((data) => {
        console.log(data);
        clearOption();
        for (i in data) {
            console.log(data[i]);
            addOption("files-dropdown", data[i],data[i]);
        }
        }
    );
}

// Monitorear el estado del procesamiento en AWS (opcional)
setInterval(() => {
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/resources/process/aws/status/download/`)
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
}, 500); // Cada 5 segundos



function downloadFilesFromAWS() {
    let streamDirectory = document.getElementById("directories-dropdown");
    let streamName = document.getElementById("files-dropdown");
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/bucket/download/transmision/`,
        {
            method: "POST",
            body: JSON.stringify(
                {
                    folder: streamDirectory.options[streamDirectory.selectedIndex].text + "high/",
                    fileName: streamName.options[streamName.selectedIndex].text.split('.').slice(0, -1).join('.')

                }
            ),
            headers: {
            "Content-type": "application/json; charset=UTF-8",
            },
        }
    ).then((response) => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("API request failed");
        }
        })
}

console.log(SERVER_IP)

getDirectoriesInDirectory()