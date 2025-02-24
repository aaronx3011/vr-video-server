const uploadButtons = document.getElementById("upload-buttons");
const dataTable = document.getElementById("main-table");
const $listServer = document
  .getElementById("list-server")
  .querySelectorAll("div");

let i = 0;

const delay = (ms) => new Promise((res) => setTimeout(res, ms));




function tableInfo() {
    cameraLinks = []
    $listServer.forEach((el) => {
        const isActive = el.querySelector("input[type=checkbox]").checked;
        const cameraURL = el.querySelector("input[type=text]").value;
        if (isActive) {
            cameraLinks.push(cameraURL);
        }
    });
    return cameraLinks
}


async function captureFrames() {
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/calibration/`, {
        method: "POST",
        body: JSON.stringify({
            cameras: tableInfo(),
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error ("Something went wrong");
        }
    })
    .then((data) => {
        alert("image code: " + data["imagesNames"]);
        console.log(data);
    })
    .catch(error => {
        alert("Error: " + error.message);
        console.log(error);
    });
}
