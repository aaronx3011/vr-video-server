const DEFAULT_CAM_COUNT = 8;

const dataTable = document.getElementById("main-table");

// $listServer removed - now handled by tab system

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

// tableInfo() function removed - replaced by new tab system implementation

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
        tableStreams.streamName
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
    const currentConfig = tableInfo();
    fetch(`http://${SERVER_IP}:${SERVER_PORT}/bucket/clear/transmision`, {

        method: "POST",
        body: JSON.stringify({
            fileName: currentConfig.streamName,
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

// --- Lógica de tabs con sincronización de datos, persistencia y compatibilidad con tableInfo() y botón global ---
(function() {
    const STORAGE_KEY = 'camera_config_sections_v1';
    const ACTIVE_KEY = 'camera_config_active_tab_v1';
    const tabBar = document.getElementById('tab-bar');
    const tabContent = document.getElementById('tab-content');
    const sectionTemplate = document.getElementById('stitching-section-template');
    const DEFAULT_CAM_COUNT = 8;

    function getDefaultSection() {
        return {
            title: 'Stitching',
            cameras: Array.from({length: DEFAULT_CAM_COUNT}, () => ({ active: false, url: '', codec: '264' })),
            streamName: '',
            alsaDevice: '',
            templateName: '',
            needsStitch: true
        };
    }

    function getCameraSection() {
        return {
            title: 'Cámara',
            camera: { cameraLink: '', codec: '264' }, // Una sola cámara
            streamName: '',
            alsaDevice: '',
            needsStitch: false
        };
    }

    function saveState(state) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    }
    function loadState() {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) return []; // Empezar vacío
        try {
            const parsed = JSON.parse(raw);
            // Migración: asegurar que todos los tabs tengan los campos nuevos
            return parsed.map((tab, index) => {
                if (index === 0) {
                    // Primer tab es siempre Stitching
                    return {
                        ...getDefaultSection(),
                        ...tab,
                        cameras: (tab.cameras && tab.cameras.length === DEFAULT_CAM_COUNT)
                            ? tab.cameras
                            : Array.from({length: DEFAULT_CAM_COUNT}, (_, i) => tab.cameras && tab.cameras[i] ? tab.cameras[i] : {active: false, url: '', codec: '264'})
                    };
                } else {
                    // Tabs adicionales son cámaras individuales
                    return {
                        ...getCameraSection(),
                        ...tab
                    };
                }
            });
        } catch {
            return [];
        }
    }
    function saveActive(idx) {
        localStorage.setItem(ACTIVE_KEY, idx);
    }
    function loadActive(max) {
        let idx = parseInt(localStorage.getItem(ACTIVE_KEY));
        if (isNaN(idx) || idx < 0) idx = 0;
        if (idx >= max + 1) idx = max;
        return idx;
    }

    // Exponer tableInfo globalmente
    window.tableInfo = function() {
        const state = loadState();
        const activeIdx = loadActive(state.length);
        
        if (activeIdx === 0) {
            // Tab de Stitching - usar configuración del estado
            const tabData = state[0] || getDefaultSection();
            return {
                needsStitch: true,
                cameras: tabData.cameras || [],
                streamName: tabData.streamName || '',
                templateName: tabData.templateName || '',
                audioDevice: tabData.alsaDevice || ''
            };
        } else {
            // Tab de cámara individual
            const tab = state[activeIdx - 1];
            return {
                needsStitch: false,
                camera: tab.camera || { cameraLink: '', codec: '264' },
                streamName: tab.streamName || '',
                audioDevice: tab.alsaDevice || ''
            };
        }
    };

    function render() {
        const state = loadState();
        let activeIdx = loadActive(state.length);
        
        // Render tab bar
        tabBar.innerHTML = '';
        
        // Primer tab fijo - Stitching (siempre presente)
        const tabStitching = document.createElement('div');
        tabStitching.className = 'flex items-center gap-1';
        const labelStitching = document.createElement('span');
        labelStitching.textContent = 'Stitching';
        labelStitching.className = 'font-bold text-white px-2 py-1 ' + (activeIdx === 0 ? 'border-b-2 border-blue-400' : 'opacity-60 hover:opacity-100 cursor-pointer');
        labelStitching.addEventListener('click', () => {
            if (activeIdx !== 0) {
                saveActive(0);
                render();
            }
        });
        tabStitching.appendChild(labelStitching);
        tabBar.appendChild(tabStitching);
        
        // Tabs dinámicos para cámaras individuales (saltar el primer tab que es Stitching)
        for (let idx = 1; idx < state.length; idx++) {
            const realIdx = idx + 1;
            const tab = document.createElement('div');
            tab.className = 'flex items-center gap-1';
            
            // Editable title
            const titleInput = document.createElement('input');
            titleInput.type = 'text';
            titleInput.value = state[idx].title;
            titleInput.className = 'bg-transparent border-b border-gray-400 px-2 py-1 font-bold text-white w-28 focus:outline-none ' + (activeIdx === realIdx ? 'border-blue-400' : '');
            titleInput.addEventListener('input', e => {
                state[idx].title = e.target.value;
                saveState(state);
            });
            
            // Cambiar de tab
            titleInput.addEventListener('focus', e => {
                if (activeIdx !== realIdx) {
                    saveActive(realIdx);
                    render();
                }
            });
            titleInput.addEventListener('click', e => {
                if (activeIdx !== realIdx) {
                    saveActive(realIdx);
                    render();
                }
            });
            tab.appendChild(titleInput);
            
            // Botón cerrar (solo para tabs de cámara individual)
            const closeBtn = document.createElement('button');
            closeBtn.textContent = '×';
            closeBtn.title = 'Cerrar pestaña';
            closeBtn.className = 'ml-1 text-red-400 hover:text-red-600 text-lg font-bold';
            closeBtn.addEventListener('click', e => {
                e.stopPropagation();
                state.splice(idx, 1);
                let newActive = activeIdx;
                if (activeIdx > state.length) newActive = state.length;
                if (newActive === 0) newActive = 0; // Siempre volver a Stitching si se cierra todo
                saveActive(newActive);
                saveState(state);
                render();
            });
            tab.appendChild(closeBtn);
            
            // Tab activa
            if (activeIdx === realIdx) {
                tab.classList.add('border-b-2', 'border-blue-500');
            } else {
                tab.classList.add('opacity-60', 'hover:opacity-100', 'cursor-pointer');
            }
            tabBar.appendChild(tab);
        }
        // Botón +
        const addBtn = document.createElement('button');
        addBtn.textContent = '+';
        addBtn.title = 'Agregar configuración de cámara';
        addBtn.className = 'ml-2 bg-blue-700 hover:bg-blue-800 text-white rounded px-3 py-1 text-lg font-bold';
        addBtn.addEventListener('click', () => {
            state.push(getCameraSection());
            saveActive(state.length);
            saveState(state);
            render();
        });
        tabBar.appendChild(addBtn);

        // Render solo la sección activa
        tabContent.innerHTML = '';
        const tabData = activeIdx === 0 ? state[0] : state[activeIdx - 1];
        const node = sectionTemplate.content.cloneNode(true);
        
        // IDs solo para el tab activo
        if (activeIdx !== 0) {
            node.querySelectorAll('[id]').forEach(el => el.removeAttribute('id'));
        }
        
        // Si no es el tab de Stitching (activeIdx !== 0), ocultar campos innecesarios
        if (activeIdx !== 0) {
            // Ocultar sección de template (mantener solo stream-name)
            const templateSection = node.querySelector('.container-action');
            if (templateSection) {
                // Ocultar todo excepto el stream-name
                const streamNameSection = templateSection.querySelector('label[for="stream-name"]')?.parentElement;
                if (streamNameSection) {
                    // Mover solo la sección de stream-name fuera del container-action
                    const streamNameClone = streamNameSection.cloneNode(true);
                    templateSection.parentNode.insertBefore(streamNameClone, templateSection);
                    templateSection.style.display = 'none';

                    // Insertar UI para una sola cámara (url + codec) justo después del stream name
                    const singleCamWrap = document.createElement('div');
                    singleCamWrap.className = 'flex flex-col gap-2 mt-4';
                    const camLabel = document.createElement('label');
                    camLabel.className = 'text-sm';
                    camLabel.textContent = 'Camera';
                    const rowDiv = document.createElement('div');
                    rowDiv.className = 'camera-card';
                    const urlInput = document.createElement('input');
                    urlInput.type = 'text';
                    urlInput.placeholder = 'camera url';
                    urlInput.className = 'w-full bg-transparent border  rounded p-[5px] pl-4 text-sm font-normal';
                    urlInput.setAttribute('data-single-camera-url', 'true');
                    const codecSelect = document.createElement('select');
                    codecSelect.className = 'test-select p-2 w-[25%] bg-transparent border border-gray-200 text-white rounded';
                    codecSelect.setAttribute('data-single-camera-codec', 'true');
                    codecSelect.innerHTML = '<option value="264">h264</option><option value="265">h265</option>';
                    rowDiv.appendChild(urlInput);
                    rowDiv.appendChild(codecSelect);
                    singleCamWrap.appendChild(camLabel);
                    singleCamWrap.appendChild(rowDiv);
                    templateSection.parentNode.insertBefore(singleCamWrap, templateSection);
                }
            }
            
            // Ocultar sección de alsa device
            const alsaSection = node.querySelector('label[for="alsa-device"]')?.parentElement;
            if (alsaSection) {
                alsaSection.style.display = 'none';
            }
            
            // Ocultar sección de cámaras
            const cameraSection = node.querySelector('.camera-list');
            if (cameraSection) {
                cameraSection.style.display = 'none';
            }
        }
        
        // Sincronizar inputs
        setTimeout(() => {
            // Stream name
            const streamSelect = document.querySelector('#stream-name');
            if (streamSelect) {
                streamSelect.value = tabData.streamName || '';
                streamSelect.addEventListener('change', e => {
                    tabData.streamName = e.target.value;
                    saveState(state);
                });
            }
            
            // Solo mostrar y sincronizar otros campos si es el tab de Stitching
            if (activeIdx === 0) {
                // Alsa device
                const alsaSelect = document.querySelector('#alsa-device');
                if (alsaSelect) {
                    alsaSelect.value = tabData.alsaDevice || '';
                    alsaSelect.addEventListener('change', e => {
                        tabData.alsaDevice = e.target.value;
                        saveState(state);
                    });
                }
                // Template file (solo nombre)
                const templateInput = document.querySelector('#template-input');
                if (templateInput) {
                    templateInput.value = '';
                    templateInput.addEventListener('change', e => {
                        tabData.templateName = e.target.files && e.target.files[0] ? e.target.files[0].name : '';
                        saveState(state);
                    });
                }
                // Cámaras
                const cameraRows = document.querySelectorAll('.camera-list > .camera-card');
                cameraRows.forEach((row, i) => {
                    const [checkbox, urlInput, select] = row.querySelectorAll('input, select');
                    if (checkbox && urlInput && select) {
                        checkbox.checked = tabData.cameras[i].active;
                        urlInput.value = tabData.cameras[i].url;
                        select.value = tabData.cameras[i].codec;
                        checkbox.addEventListener('change', e => {
                            tabData.cameras[i].active = e.target.checked;
                            saveState(state);
                        });
                        urlInput.addEventListener('input', e => {
                            tabData.cameras[i].url = e.target.value;
                            saveState(state);
                        });
                        select.addEventListener('change', e => {
                            tabData.cameras[i].codec = e.target.value;
                            saveState(state);
                        });
                    }
                });
            } else {
                // Sincronizar campos de cámara individual (no stitching)
                const singleUrl = document.querySelector('[data-single-camera-url="true"]');
                const singleCodec = document.querySelector('[data-single-camera-codec="true"]');
                if (singleUrl) {
                    singleUrl.value = (tabData.camera && tabData.camera.cameraLink) ? tabData.camera.cameraLink : '';
                    singleUrl.addEventListener('input', e => {
                        tabData.camera = tabData.camera || { cameraLink: '', codec: '264' };
                        tabData.camera.cameraLink = e.target.value;
                        saveState(state);
                    });
                }
                if (singleCodec) {
                    singleCodec.value = (tabData.camera && tabData.camera.codec) ? tabData.camera.codec : '264';
                    singleCodec.addEventListener('change', e => {
                        tabData.camera = tabData.camera || { cameraLink: '', codec: '264' };
                        tabData.camera.codec = e.target.value;
                        saveState(state);
                    });
                }
            }
        }, 0);
        tabContent.appendChild(node);
    }

    // Inicializar con estado por defecto si no existe
    let state = loadState();
    if (state.length === 0) {
        state = [getDefaultSection()];
        saveState(state);
    }
    
    // Inicializar
    render();
    // Si quieres, puedes exponer el render para debug: window.renderCameraSections = render;
    
    // Función de debug para ver el estado actual
    window.debugTabs = function() {
        const state = loadState();
        console.log('Estado actual de tabs:', state);
        console.log('Tab activo:', loadActive(state.length));
        
        // Debug detallado de cada tab
        state.forEach((tab, index) => {
            console.log(`Tab ${index}:`, {
                title: tab.title,
                type: index === 0 ? 'Stitching' : 'Cámara Individual',
                streamName: tab.streamName,
                camera: tab.camera,
                cameras: tab.cameras
            });
        });
        
        return state;
    };
})();

const allTabs = JSON.parse(localStorage.getItem('camera_config_sections_v1'));
console.log(allTabs);

function startProcess() {
    const config = tableInfo();
    // ... tu lógica aquí ...
}

function startAllTransmissions() {
    console.log('=== Iniciando startAllTransmissions ===');
    
    // Obtener el estado actual del sistema de tabs
    const state = JSON.parse(localStorage.getItem('camera_config_sections_v1')) || [];
    console.log('Estado completo de tabs:', state);
    
    const streams = [];
    
    // Agregar configuración de Stitching (siempre presente)
    const stitchingConfig = tableInfo();
    console.log('Configuración de Stitching:', stitchingConfig);
    
    if (stitchingConfig.cameras && stitchingConfig.cameras.length > 0) {
        const activeCameras = stitchingConfig.cameras.filter(cam => cam.active && cam.url);
        console.log('Cámaras activas en Stitching:', activeCameras);
        
        if (activeCameras.length > 0) {
            streams.push({
                streamConfiguration: {
                    ...stitchingConfig,
                  cameras: activeCameras
                }
            });
        }
    }
    
    // Agregar configuraciones de cámaras individuales (tabs adicionales)
    // Saltamos el primer tab (index 0) porque es el de Stitching
    console.log('Procesando tabs de cámara individual...');
    for (let i = 1; i < state.length; i++) {
        const tab = state[i];
        console.log(`Tab ${i}:`, tab);
        
        if (tab.streamName && tab.camera && tab.camera.cameraLink) {
            console.log(`Agregando cámara individual: ${tab.streamName} - ${tab.camera.cameraLink}`);
            streams.push({
                streamConfiguration: {
                    needsStitch: false,
                    camera: {
                        cameraLink: tab.camera.cameraLink,
                        codec: tab.camera.codec || '264'
                    },
                    streamName: tab.streamName,
                    audioDevice: stitchingConfig.audioDevice || ''
                }
            });
        } else {
            console.log(`Tab ${i} no cumple requisitos:`, {
                hasStreamName: !!tab.streamName,
                hasCamera: !!tab.camera,
                hasCameraLink: !!(tab.camera && tab.camera.cameraLink)
            });
        }
    }
    
    
    const finalConfig = { streams: streams };
    console.log('=== Configuración final ===');
    console.log('Total de streams:', streams.length);
    console.log('Configuración completa:', finalConfig);
    
    // Aquí puedes enviar finalConfig a tu API
    // fetch(`http://${SERVER_IP}:${SERVER_PORT}/streams/start/`, {
    //     method: "POST",
    //     body: JSON.stringify(finalConfig),
    //     headers: {
    //         "Content-type": "application/json; charset=UTF-8",
    //     },
    // });
}
