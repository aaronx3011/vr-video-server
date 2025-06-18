# Shell commands
import subprocess
import shlex
import threading

import datetime


"""
=================== COMMAND PARAMS ===================
"""



SEPARATOR = " ! "
QUEUE = "queue ! "
VIDEOCONVERT = "videoconvert"
PNGENCODER = "pngenc snapshot=true"

# TO-DO
#   
PNGSINK = "filesink location=calibration/NAME.png"


TEENAME = " tee name=tINDEX "
TEEUSE = " tINDEX."


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
            "pipe" : "nvh264dec"
        },
        {
            "codec" : "265",
            "codecName" : "nvh265dec",
            "pipe" : "nvh265dec"
        }
    ]


VIDEO = {'active': False, 'output': ''}


"""
=================== COMMAND PARAMS END ===================
"""





"""
------------------------ command generator -----------------------
"""

def inputPipeGenerator(inputLink)->tuple:
    for inputType in INPUTS_TYPES:
        if inputLink.startswith(inputType["startsWith"]):
            return inputType["pipe"].replace("INPUT", inputLink), inputType["protocolName"]

    e = Exception("Input pipeline not found", input)
    raise e




def parsePipeGenerator(inputProtocol, codec)->tuple:
    for parsePipe in DECODE_PARSE_PIPES:
        if parsePipe["inputProtocol"] == inputProtocol and parsePipe["inputCodec"] == codec:
            return parsePipe["pipe"], parsePipe["inputCodec"]

    e = Exception("Parse pipeline not found", inputProtocol, codec)
    raise e


def decoderPipeGenerator(codec)->str:
    for decodePipe in DECODE_PIPES:
        if decodePipe["codec"] == codec:
            return decodePipe["pipe"]

    e = Exception("Decoder pipeline not found", codec)
    raise e




def calibrationCommandGenerator(
        cameras: list
    )->tuple:

    commandString = "gst-launch-1.0 "
    inputCommand=""
    finalCommand=""

    imageName=str(datetime.datetime.timestamp(datetime.datetime.now())) + "-"

    teeIndex = 0

    # Input pipe
    for camera in cameras:
        cameraLink = camera["cameraLink"]
        codec = camera["codec"]

        inputCommand += inputPipeGenerator(cameraLink)[0]
        protocol = inputPipeGenerator(cameraLink)[1]
        inputCommand += SEPARATOR
        inputCommand += TEENAME.replace("INDEX", str(teeIndex))



        
        finalCommand += QUEUE 
        parseCommand, codec = parsePipeGenerator(protocol, codec)
        finalCommand += parseCommand
        finalCommand += SEPARATOR
        finalCommand += decoderPipeGenerator(codec)
        finalCommand += SEPARATOR
        finalCommand += VIDEOCONVERT
        finalCommand += SEPARATOR
        finalCommand += PNGENCODER
        finalCommand += SEPARATOR
        finalCommand += PNGSINK.replace("NAME", str(imageName) + str(teeIndex))
        

        if (teeIndex+1) < len(cameras):
            finalCommand += TEEUSE.replace("INDEX", str(teeIndex+1))
            finalCommand += SEPARATOR


        if teeIndex == len(cameras)-1:
            inputCommand += "t0."
            inputCommand += SEPARATOR



        teeIndex += 1



    commandString += inputCommand + finalCommand
    print(commandString)
    return str(commandString), str(imageName)


"""
------------------------ command generator end -----------------------
"""


def takeSnapshotStartCommand(cameras: list):
    try:
        command = calibrationCommandGenerator(cameras)[0]
        imageName = calibrationCommandGenerator(cameras)[1]
        snapshot = subprocess.Popen(
            shlex.split(command),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        for line in snapshot.stdout:
            print(line)
        return imageName
    except subprocess.CalledProcessError as e:
        raise e






"""
    # Utils
    import datetime

    # Shell commands
    import subprocess
    import shlex

    # PC interactions
    from os import getenv
    from dotenv import load_dotenv

    # Constants
    load_dotenv(".env")
    CALIBRATION_FOLDER = getenv("DEFAULT_CALIBRATION_FOLDER")

    def captureFirstFrame(inputs) -> str:
        inputsText = ""
        inputCounter = 0
        mapsText = ""
        finalCommand = "ffmpeg "
        nameSuffix=datetime.datetime.timestamp(datetime.datetime.now())
        try:
            for input in inputs:
                inputsText += f"-fflags nobuffer -flags low_delay -strict experimental -i {input} "
                mapsText += f"-map {inputCounter}:v -frames:v 1 {CALIBRATION_FOLDER}{inputCounter}-{nameSuffix}.jpg "
                inputCounter += 1

            finalCommand += inputsText + mapsText
            print(finalCommand)
            process = subprocess.Popen(shlex.split(finalCommand), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

            for line in process.stdout:
                if line.find("Error") != -1:
                    e = Exception(line)
                    raise e
            return str(nameSuffix)

        except Exception as e:
            print(e)
            raise e

"""
