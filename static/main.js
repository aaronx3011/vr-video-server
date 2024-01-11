

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



function ffmpegStart(){
    fetch('http://localhost:5000/obserffmver/start/');
    alert(';)')
}

function observerStart(){
    fetch('http://localhost:5000/observer/start/');
    alert(';)')
}

function ffmpegStop(){
    fetch('http://localhost:5000/ffmpeg/stop/');
    alert('Y-Y')
}