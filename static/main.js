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

async function updateVideo(url) {
  console.log("antes");
  await delay(10000);
  console.log("despues");
  console.log(player);
  player.src(url);
  player.load();
  player.play();
  // video.reset();
}

async function createMaster(dir, streamsDict, streamName) {
  fetch(`http://${SERVER_IP}:5000/file/create/master`, {
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
function clearOption() {
  console.log("clear");
  let selects = document.getElementsByClassName("test-select");
  console.log(selects);
  for (let i = 0; i < selects.length; i++) {
    console.log(selects[i].childElementCount);
  }

}

function addOption(text, value) {
  let selects = document.getElementsByClassName("test-select");
  for (let i = 0; i < selects.length; i++) {
    let newOption = new Option(text, value); // Create a new Option object
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
  fetch(`http://${SERVER_IP}:5000/playfab/stream/get/names`)
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("API request failed");
      }
    })
    .then((data) => {
      clearOption();
      for (i in data) {
        for (tag in data[i].Tags) {

          addOption(data[i]["Tags"][tag], data[i]["ItemId"]);
        }
      }
    });
}

setInterval(() => {
  fetch(`http://${SERVER_IP}:5000/resources/usage/`)
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
  fetch(`http://${SERVER_IP}:5000/resources/process/status/`)
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
  let streamName = document.getElementById("stream-name");
  let template = document.getElementById("template-input");
  let templateName = template.files[0].name;
  console.log(template);
  console.log(templateName);
  counter = 0;
  inputsText = "";
  filterText =
    " gldmdstitcher name=mix client=vrinsitu1 template=stitch-templates/".concat(
      templateName,
      " ! video/x-raw(memory:GLMemory),format=RGBA,width=7680,height=4320 ! tee name=t t. ! queue ! nvh265enc preset=1 ! h265parse ! hlssink2 target-duration=20 location=videos/high/8k",
      streamName.options[streamName.selectedIndex].text,
      "%05d.ts playlist-location=videos/high/8k",
      streamName.options[streamName.selectedIndex].text,
      ".m3u8 t.",
      " ! queue ! glcolorscale ! video/x-raw(memory:GLMemory),width=3840,height=2160 ! nvh265enc preset=1 ! h265parse  ! hlssink2 target-duration=20 location=videos/high/4k",
      streamName.options[streamName.selectedIndex].text,
      "%05d.ts playlist-location=videos/high/4k",
      streamName.options[streamName.selectedIndex].text,
      ".m3u8 t.",
      " ! queue ! glcolorscale ! video/x-raw(memory:GLMemory),width=2560,height=1440 ! nvh264enc preset=1 ! h264parse ! mux. autoaudiosrc ! queue ! audioconvert ! audioresample ! audio/x-raw,rate=44100,channels=2,width=16 ! avenc_aac ! aacparse ! mpegtsmux name=mux ! hlssink target-duration=20 location=videos/low/2k",
      streamName.options[streamName.selectedIndex].text,
      "%05d.ts playlist-location=videos/low/2k",
      streamName.options[streamName.selectedIndex].text,
      ".m3u8 t.",
      " ! queue ! glcolorscale ! video/x-raw(memory:GLMemory),width=1920,height=1080 ! nvh264enc preset=1 ! h264parse ! hlssink2 target-duration=20 location=videos/low/1k",
      streamName.options[streamName.selectedIndex].text,
      "%05d.ts playlist-location=videos/low/1k",
      streamName.options[streamName.selectedIndex].text,
      ".m3u8"
    );
  outputsText = "";
  let streamsToActivate = streamName.options[streamName.selectedIndex].text;

  $listServer.forEach((el) => {
    const isActive = el.querySelector("input[type=checkbox]").checked;
    const cameraURL = el.querySelector("input[type=text]").value;
    if (isActive) {
      inputsText = inputsText.concat(
        "rtmpsrc location=",
        cameraURL,
        " ! flvdemux ! h264parse ! nvh264dec ! video/x-raw(memory:GLMemory),format=NV12,width=3840,height=2160 ! glcolorconvert ! video/x-raw(memory:GLMemory),format=RGBA,width=3840,height=2160 ! mix. "
      );
    }
  });

  return [
    "gst-launch-1.0 -e ".concat(inputsText, filterText),
    streamsToActivate,
  ];
}

function updateCommand() {
  console.log(tableInfo()[0]);
}

function reloadVideo() {
  let tableStreams = tableInfo();
  updateVideo(
    `http://${SERVER_IP}:5000/file/videos/low/1k`.concat(
      tableStreams[1],
      ".m3u8"
    )
  );
}

async function stitcherStart() {
  let tableStreams = tableInfo();
  clearBucketS3();
  fetch(`http://${SERVER_IP}:5000/stitcher/start/`, {
    method: "POST",
    body: JSON.stringify({
      command: tableStreams[0],
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  });
  observerStart();
  alert(
    `http://${SERVER_IP}:5000/file/videos/low/1k`.concat(
      tableStreams[1],
      ".m3u8"
    )
  );

  updateVideo(
    `http://${SERVER_IP}:5000/file/videos/low/1k`.concat(
      tableStreams[1],
      ".m3u8"
    )
  );
  createMaster(
    "low/",
    [
      {
        bandwidth: 25000000,
        stream: "2k".concat(tableStreams[1], ".m3u8"),
      },
      {
        bandwidth: 5000000,
        stream: "1k".concat(tableStreams[1], ".m3u8"),
      },
    ],
    tableStreams[1]
  );
  createMaster(
    "high/",
    [
      {
        bandwidth: 50000000,
        stream: "8k".concat(tableStreams[1], ".m3u8"),
      },
      {
        bandwidth: 40000000,
        stream: "4k".concat(tableStreams[1], ".m3u8"),
      },
    ],
    tableStreams[1]
  );
}


async function clearFolder() {
  fetch(`http://${SERVER_IP}:5000/file/clear/videos`);
}

async function clearBucketS3() {
  fetch(`http://${SERVER_IP}:5000/bucket/clear/transmision`, {

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
  fetch(`http://${SERVER_IP}:5000/observer/start/`);
}

function stitcherStop() {
  fetch(`http://${SERVER_IP}:5000/stitcher/stop/`, {
    method: "POST",
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  });
  alert("Y-Y");
}
function observerStop() {
  fetch(`http://${SERVER_IP}:5000/observer/stop/`);
}
function updatePath() {
  console.log(template);
}

getStreamNames();