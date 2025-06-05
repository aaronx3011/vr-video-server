# Shell commands
import subprocess
import shlex
import threading

SEPARATOR = " ! "
QUEUE = "queue ! "

MUX = "mpegtsmux name=MUXNAME"

DEFAULT_COLOR = "RGBA"

OUTPUT_RESOLUTIONS = ["8k", "4k", "2k", "1k"]

STITCHER_PIPE = "gldmdstitcher name=mix client=vrinsitu1 template=stitch-templates/TEMPLATE crop-left=-90 crop-right=90 crop-bottom=-45 crop-top=45"

# STITCHER_PIPE = "gldmdstitcher name=mix client=vrinsitu1 template=stitch-templates/TEMPLATE crop-left=-67 crop-right=67 crop-bottom=-40 crop-top=40"

# STITCHER_PIPE = "gldmdstitcher name=mix client=vrinsitu1 template=stitch-templates/TEMPLATE crop-left=-67 crop-right=67 crop-bottom=-20 crop-top=20"

# STITCHER_PIPE = "gldmdstitcher name=mix client=vrinsitu1 template=stitch-templates/TEMPLATE"
STITCHER_FORMAT_PIPE = "video/x-raw(memory:GLMemory),format=RGBA,width=7680,height=4320 ! tee name=t t."

COLOR_CONVERT = "glcolorconvert ! video/x-raw(memory:GLMemory),format=COLORFORMAT"
COLOR_SCALE = "glcolorscale ! video/x-raw(memory:GLMemory), width=WIDTH, height=HEIGHT"

AUDIO_PIPE = "alsasrc device=hw:DEVICE ! queue ! audioconvert ! audioresample ! audio/x-raw,rate=48000,channels=2,width=16 ! avenc_aac ! aacparse ! tee name=at at."


INPUTS_TYPES = [
        {
            "startsWith" : "rtsp://",
            "protocolName" : "RTSP",
            "pipe" : "rtspsrc location=INPUT"
        },
        {
            "startsWith" : "rtmp://",
            "protocolName" : "RTMP",
            "pipe" : "rtmpsrc location=INPUT"
        }
    ]

DECODE_PARSE_PIPES = [
        {
            "inputProtocol" : "RTSP",
            "inputCodec" : "264",
            "pipe" : "rtph264depay ! h264parse"
        },
        {
            "inputProtocol" : "RTSP",
            "inputCodec" : "265",
            "pipe" : "rtph265depay ! h265parse"
        },
        {
            "inputProtocol" : "RTMP",
            "inputCodec" : "264",
            "pipe" : "flvdemux ! h264parse"
        },
        {
            "inputProtocol" : "RTMP",
            "inputCodec" : "265",
            "pipe" : "flvdemux ! h265parse"
        }
    ]

DECODE_PIPES = [
        {
            "codec" : "264",
            "codecName" : "nvh264dec",
            "pipe" : "nvh264dec ! video/x-raw(memory:GLMemory)"
        },
        {
            "codec" : "265",
            "codecName" : "nvh265dec",
            "pipe" : "nvh265dec ! video/x-raw(memory:GLMemory)"
        }
    ]



RESOLUTIONS = {
        "8k": {
            "resolution" : "8k",
            "resolutionName" : "8k",
            "preferedCodec": "265",
            "width": "8001",
            "height": "3960"
            },
        "4k": {
            "resolution" : "4k",
            "resolutionName" : "4k",
            "preferedCodec": "265",
            "width": "3840",
            "height": "2160"
            },
        "2k": {
            "resolution" : "2k",
            "resolutionName" : "2k",
            "preferedCodec": "264",
            "width": "2560",
            "height": "1440"
            },
        "1k": {
            "resolution" : "1k",
            "resolutionName" : "1k",
            "preferedCodec": "264",
            "width": "2600",
            "height": "900"
            }
        }

MP4_SINK_PIPES = {
        "8k": {
            "resolution" : "8k",
            "resolutionName" : "8k",
            "folder" : "videos/high",
            "pipe" : "filesink location=videos/high/8kFILENAME.mp4"
            },
        "4k": {
            "resolution" : "4k",
            "resolutionName" : "4k",
            "folder" : "videos/high",
            "pipe" : "filesink location=videos/high/4kFILENAME.mp4"
            },
        "2k": {
            "resolution" : "2k",
            "resolutionName" : "2k",
            "folder" : "videos/low",
            "pipe" : "filesink location=videos/low/2kFILENAME.mp4"
            },
        "1k": {
            "resolution" : "1k",
            "resolutionName" : "1k",
            "folder" : "videos/low",
            "pipe" : "filesink location=videos/low/1kFILENAME.mp4"
            }
        }

HLS_SINK_PIPES = {
        "8k": {
            "resolution" : "8k",
            "resolutionName" : "8k",
            "folder" : "videos/high",
            "pipe" : "hlssink target-duration=15 location=videos/high/8kFILENAME%05d.ts playlist-location=videos/high/8kFILENAME.m3u8"
            },
        "4k": {
            "resolution" : "4k",
            "resolutionName" : "4k",
            "folder" : "videos/high",
            "pipe" : "hlssink target-duration=15 location=videos/high/4kFILENAME%05d.ts playlist-location=videos/high/4kFILENAME.m3u8"
            },
        "2k": {
            "resolution" : "2k",
            "resolutionName" : "2k",
            "folder" : "videos/low",
            "pipe" : "hlssink target-duration=15 location=videos/low/2kFILENAME%05d.ts playlist-location=videos/low/2kFILENAME.m3u8"
            },
        "1k": {
            "resolution" : "1k",
            "resolutionName" : "1k",
            "folder" : "videos/low",
            "pipe" : "hlssink target-duration=15 location=videos/low/1kFILENAME%05d.ts playlist-location=videos/low/1kFILENAME.m3u8"
            }
        }

ENCODE_PIPES = {
        "264": {
            "codec" : "264",
            "codecName" : "nvh264enc",
            "pipe" : "nvh264enc preset = 1 ! h264parse"
            },
        "265": {
            "codec" : "265",
            "codecName" : "nvh265enc",
            "pipe" : "nvh265enc preset = 1 ! h265parse"
            }
        }


VIDEO = {'active': False, 'output': ''}


"""
------------------------ command generation -----------------------
"""

def stitcherInputPipeGenerator(inputLink)->tuple:
    for inputType in INPUTS_TYPES:
        if inputLink.startswith(inputType["startsWith"]):
            return inputType["pipe"].replace("INPUT", inputLink), inputType["protocolName"]

    e = Exception("Input pipeline not found", input)
    raise e




def stitcherParsePipeGenerator(inputProtocol, codec)->tuple:
    for parsePipe in DECODE_PARSE_PIPES:
        if parsePipe["inputProtocol"] == inputProtocol and parsePipe["inputCodec"] == codec:
            return parsePipe["pipe"], parsePipe["inputCodec"]

    e = Exception("Parse pipeline not found", inputProtocol, codec)
    raise e


def stitcherDecorderPipeGenerator(codec)->str:
    for decodePipe in DECODE_PIPES:
        if decodePipe["codec"] == codec:
            return decodePipe["pipe"]

    e = Exception("Decoder pipeline not found", codec)
    raise e


def stitcherGlColorConvertPipeGenerator(colorFormat):
    return COLOR_CONVERT.replace("COLORFORMAT", colorFormat)




def stitcherCommandGenerator(
        cameras: list,
        templateName:str = 'template.pts',
        streamName:str = 'live',
        audioDevice:int = 0,
        outputformat: str = 'hls',
        outputResolutions: list = OUTPUT_RESOLUTIONS
    )->str:

    commandString = "gst-launch-1.0 -e "

    mixIndex = 0
    # Input pipe
    for camera in cameras:
        cameraLink = camera["cameraLink"]
        codec = camera["codec"]
        if mixIndex != 0:
            commandString += "mix. "

        inputCommand, protocol = stitcherInputPipeGenerator(cameraLink)
        inputCommand += SEPARATOR
        parseCommand, codec = stitcherParsePipeGenerator(protocol, codec)
        inputCommand += parseCommand
        inputCommand += SEPARATOR
        inputCommand += stitcherDecorderPipeGenerator(codec)
        inputCommand += SEPARATOR
        inputCommand += stitcherGlColorConvertPipeGenerator(DEFAULT_COLOR)
        inputCommand += SEPARATOR

        commandString += inputCommand

        mixIndex += 1


    commandFinalString = commandString + ""

    # Stitch pipe
    commandFinalString += "mix. "
    commandFinalString += STITCHER_PIPE.replace("TEMPLATE", templateName)
    commandFinalString += SEPARATOR
    commandFinalString += STITCHER_FORMAT_PIPE
    commandFinalString += SEPARATOR

    # Encoder pipe

    # 8k pipe
    resolutionIndex = 0
    for output in OUTPUT_RESOLUTIONS:
        muxName = "mux" + str(resolutionIndex)
        commandFinalString += QUEUE
        if resolutionIndex != 0:
            commandFinalString += COLOR_SCALE.replace("WIDTH", RESOLUTIONS[output]["width"]).replace("HEIGHT", RESOLUTIONS[output]["height"])
            commandFinalString += SEPARATOR
        commandFinalString += ENCODE_PIPES[RESOLUTIONS[output]["preferedCodec"]]["pipe"]
        commandFinalString += SEPARATOR

        if resolutionIndex == 0:
            commandFinalString += QUEUE
            commandFinalString += muxName + ". "
            commandFinalString += AUDIO_PIPE.replace("DEVICE", audioDevice)

        else:
            commandFinalString +="muxINDEX. at.".replace("INDEX", str(resolutionIndex))

        commandFinalString += SEPARATOR
        commandFinalString += QUEUE
        commandFinalString += MUX.replace("MUXNAME", muxName)
        commandFinalString += SEPARATOR
        commandFinalString += HLS_SINK_PIPES[output]["pipe"].replace("FILENAME", streamName)

        if output != OUTPUT_RESOLUTIONS[-1]:
            commandFinalString += " t."
            commandFinalString += SEPARATOR


        resolutionIndex += 1
    return commandFinalString


def stitcherStartCommand(stitcherCommand):
    try:
        process = subprocess.Popen(shlex.split(stitcherCommand), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            VIDEO["output"] = line[:-1]
        VIDEO["active"] = False
        VIDEO["output"] = ""
    except subprocess.CalledProcessError as e:
        raise e
    return True

def stitcherStart(stitcherCommand):
    try:
        if VIDEO['active'] == False:
            x = threading.Thread(target=stitcherStartCommand, args= (stitcherCommand,))
            x.start()
            VIDEO['active'] = True
        else:
            e = subprocess.CalledProcessError(999, "", "This process is already running", "This process is already running")
            raise e
    except subprocess.CalledProcessError as e:
        raise e

def stitcherStop():
    try:
        subprocess.check_call(['pkill', 'gst'], stdout= subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise e

