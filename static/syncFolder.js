async function syncFolders(){
    let folderInput = document.getElementById("folder-name-input");
    let folderName = folderInput.value
    fetch(`http://${SERVER_IP}:5000/bucket/sync/${folderName}`,{method: "POST"})
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
            document.getElementById("aws-status").textContent=data["text"];
        })
        .catch(error => {
            console.error(error);
        });

}, 50);