const uploadButtons = document.getElementById("upload-buttons");
const dataTable = document.getElementById("main-table");
const $listServer = document
  .getElementById("list-server")
  .querySelectorAll("div");

let i = 0;

const delay = (ms) => new Promise((res) => setTimeout(res, ms));





function tableInfo() {
    let cameras = [];

    $listServer.forEach((el) => {
        const isActive = el.querySelector("input[type=checkbox]").checked;
        if (isActive == true) {
            const cameraURL = el.querySelector("input[type=text]").value;
            const codecSelected = el.querySelector("select").value;
            cameras.push({cameraLink: cameraURL, codec: codecSelected});
        }

    });

    return cameras;
}

function updateCommand() {
    console.log(tableInfo());
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









/*
async function stitcherStart() {
    let tableStreams = tableInfo();
    clearBucketS3();
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/stitcher/start/`, {
        method: "POST",
        body: JSON.stringify({
            streamConfiguration: tableStreams,
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
        },
    }). then((response) => {
        if (response.ok) return response.json();
        else throw new Error("API request failed");
    }).then((data)=> {
        console.log(data);
    });
    observerStart();
    alert(
        `http://${SERVER_IP}:${SERVER_PORT}/file/videos/low/1k`.concat(
            tableStreams.streamName,
            ".m3u8"
        )
    );

    updateVideo(
        `http://${SERVER_IP}:${SERVER_PORT}/file/videos/low/1k`.concat(
            tableStreams.streamName,
            ".m3u8"
        )
    );
    createMaster(
        "low/",
        [
            {
                bandwidth: 20000000,
                stream: "2k".concat(tableStreams.streamName, ".m3u8"),
            },
            {
                bandwidth: 10000000,
                stream: "1k".concat(tableStreams.streamName, ".m3u8"),
            },
        ],
        tableStreams[1]
    );
    createMaster(
        "high/",
        [
            {
                bandwidth: 45000000,
                stream: "8k".concat(tableStreams.streamName, ".m3u8"),
            },
            {
                bandwidth: 25000000,
                stream: "4k".concat(tableStreams.streamName, ".m3u8"),
            },
        ],
        tableStreams.streamName
    );
}


async function clearFolder() {
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/file/clear/videos`);
}

async function clearBucketS3() {
    console.log(`http://${SERVER_IP}:${SERVER_PORT}/bucket/clear/transmision`);
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/bucket/clear/transmision`, {

        method: "POST",
        body: JSON.stringify({
            fileName: document.getElementById("stream-name").options[document.getElementById("stream-name").selectedIndex].text,
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
        },
    });
}

async function observerStart() {
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/observer/start/`);
}

async function backupBucket() {
    const textLink = document.getElementById("title-backup");
    const spinner = document.querySelector(".loader");
    const backupButton = document.getElementById("backup-bucket-button");

    console.log("backupBucket");

    backupButton.disabled = true;
    spinner.classList.replace("hidden", "block");
    textLink.classList.replace("flex", "hidden");
    try {
        await fetch(`http://${SERVER_IP}:${SERVER_PORT}/bucket/sync/transmision`,{method: "POST"})
            .then(data => {
                alert(":)");
            })
    .catch(error => {
        console.log(error);
    });

    } catch (err) {
        alert(err);
    } finally {
        textLink.classList.replace( "hidden","flex");
        spinner.classList.replace( "block","hidden");
    }
}


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
            document.getElementById("aws-status").textContent=data["text"];
        })
        .catch(error => {
            console.error(error);
        });

}, 500);


function stitcherStop() {
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/stitcher/stop/`, {
        method: "POST",
        headers: {
            "Content-type": "application/json; charset=UTF-8",
        },
    });
    alert("Y-Y");
}
function observerStop() {
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/observer/stop/`);
}
function updatePath() {
    console.log(template);
}

getStreamNames();
getAlsaDevices();


*/
