async function uploadStart(){
    let file = document.getElementById("template-input");
    let fileName = file.files[0].name
    fetch(`http://${SERVER_IP}:5000/publicidad/start/`,
        {
            method: "POST",
            body: JSON.stringify({
                command: "ffmpeg -i ./publicidad/".concat(fileName, " -c:v libx264 ./publicidad/", fileName.substring(0,fileName.lastIndexOf('.')), ".m3u8")
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }
    )
    .then(data => {
        alert(":)");
    })
    .catch(error => {
        alert(error);
        console.log(error);
    });
}


setInterval(() => {
    fetch(`http://${SERVER_IP}:5000/publicidad/status/`)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('API request failed');
            }
        })
        .then(data => {
            document.getElementById("ffmpeg-text").textContent=data["text"];
        })
        .catch(error => {
            console.error(error);
        });

}, 50);