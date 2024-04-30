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

    // let optionsToDelete = document.getElementsByTagName('option')

    // for (let i = 0; i < optionsToDelete.length; i++){
    //     optionsToDelete[i].remove()
    // }

}


function addOption(text,value){
    let selects = document.getElementsByClassName("test-select");
    for (let i = 0; i < selects.length; i++){
        // console.log(selects[i])
        let newOption = new Option(text, value); // Create a new Option object
        selects[i].appendChild(newOption);
    }
}

function addData(chart/*, label*/, newData) {
    //chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(newData);
    });
    chart.update();
}

function removeData(chart) {
    //chart.data.labels.pop();
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
                    // console.log(data[i].Tags[tag]);

                    addOption(data[i]['Tags'][tag],data[i]["ItemId"]);
                }
            };
    })
}

setInterval(() => {
    fetch('http://172.16.0.78:5000/resources/')
        .then(response => {
            if (response.ok) {
            return response.json(); // Parse the response data as JSON
            } else {
            throw new Error('API request failed');
            }
        })
        .then(data => {
            // Process the response data here
            // Example: Logging the data to the console
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
            // if (varGPU.length > 9){
            //     varGPU.splice(-1);
            // }
            // if (varRAM.length > 9){
            //     varRAM.splice(-1);
            // }


            i++;
            addData(chart,Number(data["utilization.gpu [%]"]));
            // varGPU.unshift(Number(data["utilization.gpu [%]"]));
            // varRAM.unshift(Number(data["utilization.ram [%]"]));
            //chart.update();

        })
        .catch(error => {
            // Handle any errors here
            console.error(error); // Example: Logging the error to the console
        });

}, 500);




setInterval(() => {
    fetch('http://172.16.0.78:5000/ffmpeg/status/')
        .then(response => {
            if (response.ok) {
            return response.json(); // Parse the response data as JSON
            } else {
            throw new Error('API request failed');
            }
        })
        .then(data => {
            // Process the response data here
            // Example: Logging the data to the console
            document.getElementById("ffmpeg-text").textContent=data["text"];
            document.getElementById("observer-text").textContent=data["observerText"];
        })
        .catch(error => {
            // Handle any errors here
            console.error(error); // Example: Logging the error to the console
        });

}, 50);


function tableInfo(){

    counter = 0;
    inputsText = "";
    filterText = " -filter_complex '";
    outputsText = "";
    let videoWidth = document.getElementById("width").value;
    let videoHeight = document.getElementById("height").value;
    let streamsToActivate=[];

    for (row = 0; row < dataTable.rows.length; row++){
        if(dataTable.rows[row].cells[0].children[0].checked== true){
            counter ++;
            inputsText = inputsText.concat(
                " -thread_queue_size 4096 -rtsp_transport tcp -i ",
                dataTable.rows[row].cells[1].children[0].value 
            );
            if(row != 0) {filterText = filterText.concat(";");}
            filterText = filterText.concat(
                "[", row, ":v]split=2[v",row,"][preview", row, "];[preview", row, "]scale=w=1280:h=720[scale", row, "]"
            );
            outputsText = outputsText.concat(
                "-map '[v", row,"]' -c:v ",
                dataTable.rows[row].cells[2].children[0].value, " ",
                "-maxrate ", dataTable.rows[row].cells[3].children[0].value, "M ",
                "videos/", dataTable.rows[row].cells[4].children[0].value, ".m3u8 ",
                // Preview
                "-map '[scale", row,"]' -c:v ",
                "libx264", " ",
                "-maxrate ", "1M ",
                "videos/preview", dataTable.rows[row].cells[4].children[0].value, ".m3u8 "
            );
            streamsToActivate.push(dataTable.rows[row].cells[4].children[0].value)
        }
    }
    // if (counter == 1) {
    //     return ["ffmpeg -hwaccel cuda ".concat(inputsText, " -vf 'scale=",videoWidth,":",videoHeight,"'", outputsText.substr(11)), streamsToActivate];
    // }
    return ["ffmpeg -hwaccel cuda ".concat(inputsText, filterText, "' ", outputsText), streamsToActivate];
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
            return response.json(); // Parse the response data as JSON
            } else {
            throw new Error('API request failed');
            }
        })
        .then(data => {
            // Process the response data here
            // Example: Logging the data to the console
            console.log(tableStreams[1][stream], data["success"])
        })
        .catch(error => {
            // Handle any errors here
            console.error(error); // Example: Logging the error to the console
        });
    }
    
    videoSource.setAttribute('src','http://172.16.0.78:5000/file/preview/preview'.concat(tableStreams[1], '.m3u8'))

    // alert('http://172.16.0.78:5000/file/preview/preview'.concat(tableStreams[1], '.m3u8'));

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

// console.log(tableInfo());
getStreamNames();