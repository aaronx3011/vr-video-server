async function uploadStart(){
    let file = document.getElementById("template-input");
    let fileName = file.files[0].name
    fetch(`http://${SERVER_IP}:5000/bucket/sync/banners`,{method: "POST"})
    .then(data => {
        alert(":)");
    })
    .catch(error => {
        alert(error);
        console.log(error);
    });
}


setInterval(() => {
    fetch(`http://${SERVER_IP}:5000/resources/process/aws/status/`)
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