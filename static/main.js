const dataTable = document.getElementById("main-table");

setInterval(() => {
    fetch('http://localhost:5000/resources/')
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
        })
        .catch(error => {
            // Handle any errors here
            console.error(error); // Example: Logging the error to the console
        });

}, 500);




setInterval(() => {
    fetch('http://localhost:5000/ffmpeg/status/')
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

    inputsText = "";
    filterText = " -filter_complex '";
    outputsText = "";

    for (row = 0; row < dataTable.rows.length; row++){
        if(dataTable.rows[row].cells[0].children[0].checked== true){
            inputsText = inputsText.concat(
                " -thread_queue_size 4096 -rtsp_transport tcp -i ",
                dataTable.rows[row].cells[1].children[0].value 
            );
            if(row != 0) {filterText = filterText.concat(";");}
            filterText = filterText.concat(
                "[", row, ":v]copy[v",row,"]"
            );
            outputsText = outputsText.concat(
                "-map '[v", row,"]' -c:v ",
                dataTable.rows[row].cells[2].children[0].value, " ",
                "-maxrate ", dataTable.rows[row].cells[3].children[0].value, "M ",
                "videos/", dataTable.rows[row].cells[4].children[0].value, ".m3u8 "
            );
        }
    }
    return "ffmpeg ".concat(inputsText, filterText, "' ", outputsText);
}


async function ffmpegStart(){

    fetch("http://localhost:5000/ffmpeg/start/", {
        method: "POST",
        body: JSON.stringify({
            command: tableInfo()
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
        });
    observerStart();
    alert(';)');    
}



async function observerStart(){
    fetch('http://localhost:5000/observer/start/');
    alert(';)')
}

function ffmpegStop(){
    fetch('http://localhost:5000/ffmpeg/stop/');
    alert('Y-Y')
}

console.log(tableInfo());