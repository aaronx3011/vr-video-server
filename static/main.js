const dataTable = document.getElementById("main-table");

const $listServer = document
    .getElementById("list-server")
    .querySelectorAll("div");

const $cameras = document.querySelectorAll(".cam");
const command = document.getElementById("command-span");
const videoSource = document.getElementById("video-source");
const video = document.getElementById("my-video");
let i = 0;
let streamsNames = [];

const delay = (ms) => new Promise((res) => setTimeout(res, ms));

const $navbar = document.querySelector("#navbar");
const $buttonNav = document.getElementById("openNav");

let isOpen = false;
$buttonNav.addEventListener("click", (e) => {

    console.log("console.log()")

    $navbar.classList.toggle("h-[80px]")
    isOpen = false;


})

async function updateVideo(url) {
    console.log("antes");
    await delay(10000);
    console.log("despues");
    console.log(player);
    player.src(url);
    player.load();
    player.play();
}

async function createMaster(dir, streamsDict, streamName) {
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/file/create/master`, {
        method: "POST",
        body: JSON.stringify({
            fileName: dir.concat(streamName, ".m3u8"),
            streams: streamsDict,
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
        },
    });
}

window.onload = () => {

    $cameras.forEach((el) => {
        const id = el.id;
        const path = window.location.pathname;

        if (String(path).includes(id)) {
            el.classList.replace("bg-white/0", "bg-white/30");
        } else {
            el.classList.replace("bg-white/30", "bg-white/0");
        }
    });
};
function clearOption(className) {
    console.log("clear");
    let selects = document.getElementsByClassName(className);
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

function addData(chart, newData) {
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(newData);
    });
    chart.update();
}

function removeData(chart) {
    chart.data.datasets.forEach((dataset) => {
        dataset.data.shift();
    });
    chart.update();
}

function getStreamNames() {
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/playfab/stream/get/names`)
        .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error("API request failed");
            }
        })
        .then((data) => {
            clearOption("stream-select");
            for (i in data) {
                for (tag in data[i].Tags) {
                    addOption("stream-select", data[i]["Tags"][tag], data[i]["ItemId"]);
                }
            }
        });
}

function getAlsaDevices() {
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/audio/record/devices/`)
        .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error("API request failed");
            }
        })
        .then((data) => {
            clearOption("stream-select");
            for (i=0; i< data.length; i++) {
                addOption("alsa-record-devices", data[i]["name"], data[i]["index"]);
            }
        });
}
setInterval(() => {
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/resources/usage/`)
        .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error("API request failed");
            }
        })
        .then((data) => {
            document.getElementById("cpu").textContent = data["utilization.cpu [%]"];
            document.getElementById("ram").textContent = data["utilization.ram [%]"];
            document.getElementById("gpu").textContent = data["utilization.gpu [%]"];
            document.getElementById("encoder").textContent = data["utilization.encoder [%]"];
            document.getElementById("decoder").textContent = data["utilization.decoder [%]"];
            document.getElementById("vram").textContent = data["utilization.memory [%]"];

            if (i > 30) {
                removeData(chart);
                i--;
            }

            i++;
            addData(chart, Number(data["utilization.gpu [%]"]));
        })
        .catch((error) => {
            console.error(error);
        });
}, 500);

function changeCamera(e) {
    window.location.href = `/stream/${e}`;
}

setInterval(() => {
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/resources/process/status/`)
        .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error("API request failed");
            }
        })
        .then((data) => {
            document.getElementById("ffmpeg-text").textContent = data["text"];
            document.getElementById("observer-text").textContent = data["observerText"];
        })
        .catch((error) => {
            console.error(error);
        });
}, 100);

function tableInfo() {
    let streamName = document.getElementById("stream-name").options[document.getElementById("stream-name").selectedIndex].text;
    let template = document.getElementById("template-input");
    let templateName = template.files[0].name;
    let audioDevice = document.querySelector("#alsa-device").value;
    let cameras = [];

    console.log(templateName);
    $listServer.forEach((el) => {
        const isActive = el.querySelector("input[type=checkbox]").checked;
        if (isActive == true) {
            const cameraURL = el.querySelector("input[type=text]").value;
            const codecSelected = el.querySelector("select").value;
            cameras.push({cameraLink: cameraURL, codec: codecSelected});
        }

    });

    return {cameras: cameras, templateName: templateName, streamName: streamName, audioDevice: audioDevice};
}

function updateCommand() {
    console.log(tableInfo());
}

function reloadVideo() {
    let tableStreams = tableInfo();
    updateVideo(
        `http://${SERVER_IP}:${SERVER_PORT}/file/videos/low/1k`.concat(
            tableStreams.streamName,
            ".m3u8"
        )
    );
}

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
