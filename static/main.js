const dataTable = document.getElementById("main-table");
const command = document.getElementById("command-span");
const videoSource = document.getElementById("video-source");
let i =0;
let streamsNames = []

function clearOption(){
    console.log("clear")
    let selects = document.getElementsByClassName("test-select");
    console.log(selects);
    for (let i = 0; i < selects.length; i++){
        console.log(selects[i].childElementCount);
    }
}


function addOption(text,value){
    let selects = document.getElementsByClassName("test-select");
    for (let i = 0; i < selects.length; i++){
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

function getStreamNames(){

    fetch('http://172.16.0.78:5000/playfab/stream/get/names')
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('API request failed');
        }
    })
    .then(data => {
        clearOption();
            for (i in data){
                for (tag in data[i].Tags){
                    addOption(data[i]['Tags'][tag],data[i]["ItemId"]);
                }
            };
    })
}

setInterval(() => {
    fetch('http://172.16.0.78:5000/resources/')
        .then(response => {
            if (response.ok) {
            return response.json();
            } else {
            throw new Error('API request failed');
            }
        })
        .then(data => {
            document.getElementById("cpu").textContent=data["utilization.cpu [%]"];
            document.getElementById("ram").textContent=data["utilization.ram [%]"];
            document.getElementById("gpu").textContent=data["utilization.gpu [%]"];
            document.getElementById("encoder").textContent=data["utilization.encoder [%]"];
            document.getElementById("decoder").textContent=data["utilization.decoder [%]"];
            document.getElementById("vram").textContent=data["utilization.memory [%]"];
            if (i > 30){
                removeData(chart);
                i--;
            }
            i++;
            addData(chart,Number(data["utilization.gpu [%]"]));
        })
        .catch(error => {
            console.error(error);
        });

}, 500);




setInterval(() => {
    fetch('http://172.16.0.78:5000/ffmpeg/status/')
        .then(response => {
            if (response.ok) {
            return response.json();
            } else {
            throw new Error('API request failed');
            }
        })
        .then(data => {
            document.getElementById("ffmpeg-text").textContent=data["text"];
            document.getElementById("observer-text").textContent=data["observerText"];
        })
        .catch(error => {
            console.error(error);
        });

}, 50);


function tableInfo(){
    let streamName= document.getElementById("stream-name")
    counter = 0;
    inputsText = "";
    filterText = " glvideomixer2 name=mix ! video/x-raw\(memory:GLMemory\),format=RGBA,width=7680,height=4320 ! nvh265enc preset=1 ! h265parse ! hlssink2 target-duration=2 location=videos/%05d.ts playlist-location=videos/".concat(streamName.options[streamName.selectedIndex].text, ".m3u8");
    outputsText = "";
    let streamsToActivate=[streamName.value];

    for (row = 0; row < dataTable.rows.length; row++){
        for (row = 0; row < dataTable.rows.length; row++){
            if(dataTable.rows[row].cells[0].children[0].checked== true){
                counter ++;
                inputsText = inputsText.concat(
                    "rtmpsrc location=",
                    dataTable.rows[row].cells[1].children[0].value,
                    " ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\),format=NV12,width=3840,height=2160 ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA,width=3840,height=2160 ! mix. "
                );
            }
        }
    }
    return ["gst-launch-1.0 -e ".concat(inputsText, filterText), streamsToActivate];
}

function updateCommand(){
    command.textContent=tableInfo()[0];
}

async function ffmpegStart(){

    let tableStreams=tableInfo()
    clearBucketS3(); 
    fetch("http://172.16.0.78:5000/ffmpeg/start/", {
        method: "POST",
        body: JSON.stringify({
            command: tableStreams[0]
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
        });
    observerStart();
    for (stream in tableStreams[1]){
        fetch('http://172.16.0.78:5000/playfab/stream/'.concat(tableStreams[1][stream], '/on/'))
        .then(response => {
            if (response.ok) {
            return response.json();
            } else {
            throw new Error('API request failed');
            }
        })
        .then(data => {
            console.log(tableStreams[1][stream], data["success"])
        })
        .catch(error => {
            console.error(error);
        });
    }
    
    videoSource.setAttribute('src','http://172.16.0.78:5000/file/preview/preview'.concat(tableStreams[1], '.m3u8'))

}


async function clearBucketS3(){
    fetch('http://172.16.0.78:5000/bucket/clear/');
}


async function observerStart(){
    fetch('http://172.16.0.78:5000/observer/start/');
}

function ffmpegStop(){
    fetch('http://172.16.0.78:5000/ffmpeg/stop/');
    alert('Y-Y')
}
getStreamNames();