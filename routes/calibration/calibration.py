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
            inputsText += f"-i {input} "
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
