# Utils
import time

# Shell commands
import subprocess
import shlex

# PC interactions
import os
from dotenv import load_dotenv



DEFAULT_BUCKET_LINK = os.getenv("DEFAULT_BUCKET_LINK") 
DEFAULT_DOWNLOAD_FOLDER = os.getenv("DEFAULT_DOWNLOAD_FOLDER")
AWS = {"active": False, "output" : ""}
AWS_DOWNLOAD = {"active": False, "output" : ""}


def clearFilesByNameRecursive(folder, fileName):
    try:
        command = f"aws s3 rm {DEFAULT_BUCKET_LINK}/{folder} --exclude '*' --include '*{fileName}*' --recursive"
        subprocess.Popen(
            shlex.split(command),
            stdout=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        raise e

def clearFilesByName(folder, fileName):
    try:
        command = f"aws s3 rm {DEFAULT_BUCKET_LINK}/{folder} --exclude '*' --include '*{fileName}*'"
        subprocess.Popen(
            shlex.split(command),
            stdout=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        raise e

def syncFromLocalFolderToAWS(folder):
    try:
        command = f"aws s3 sync ./{folder} {DEFAULT_BUCKET_LINK}/{folder}" 
        process = subprocess.Popen(
            shlex.split(command),
            stdout=subprocess.PIPE
        )
        for line in process.stdout:
            pass
    except subprocess.CalledProcessError as e:
        raise e

def syncFromAWSFolderToAWS(folder):
    try:
        if AWS['active'] == False:
            AWS['active'] == True
            command = f"aws s3 sync {DEFAULT_BUCKET_LINK}/{folder} {DEFAULT_BUCKET_LINK}/{folder}{time.time()}" 
            process = subprocess.Popen(
                shlex.split(command),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            for line in process.stdout:
                AWS['output'] = line[:-1]
            AWS['active'] = False
            AWS['output'] = ""
    except subprocess.CalledProcessError as e:
        raise e

def listObjectInDirectory(directory):
    command = f"aws s3 ls {DEFAULT_BUCKET_LINK}{directory}"
    print(command)
    try:
        procces = subprocess.Popen(
            shlex.split(command),
            stdout=subprocess.PIPE
        ).communicate()[0]

        return [key[(key.rfind(' ') + 1):] for key in procces.decode("utf-8").split("\n")]
    except subprocess.CalledProcessError as e:
        raise e

def listDirectoriesInDirectory(directory=""):
    command = f"aws s3 ls {DEFAULT_BUCKET_LINK}{directory}"
    try:
        procces = subprocess.Popen(
            shlex.split(command),
            stdout=subprocess.PIPE,
        )
        outputFilter = subprocess.Popen(['grep', '/'], stdin = procces.stdout, stdout = subprocess.PIPE).communicate()[0]

        return [key[(key.rfind(' ') + 1):] for key in outputFilter.decode("utf-8").split("\n")]

    except subprocess.CalledProcessError as e:
        raise e


def listPlaylistsInDirectory(directory):
    command = f"aws s3 ls {DEFAULT_BUCKET_LINK}{directory}"
    try:
        procces = subprocess.Popen(
            shlex.split(command),
            stdout=subprocess.PIPE,
        )
        outputFilter = subprocess.Popen(['grep', '.m3u8'], stdin = procces.stdout, stdout = subprocess.PIPE).communicate()[0]

        return [key[(key.rfind(' ') + 1):] for key in outputFilter.decode("utf-8").split("\n")]

    except subprocess.CalledProcessError as e:
        raise e


def downloadFilesFromAWSByName(AWSFolder, fileName):
    try:
        if AWS_DOWNLOAD['active'] == False:
            AWS_DOWNLOAD['active'] == True
            command = f"aws s3 sync {DEFAULT_BUCKET_LINK}{AWSFolder} ./{DEFAULT_DOWNLOAD_FOLDER} --exclude '*' --include '*{fileName}*'"
            process = subprocess.Popen(
                shlex.split(command),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            for line in process.stdout:
                AWS_DOWNLOAD['output'] = line[:-1]
            AWS_DOWNLOAD['active'] = False
            AWS_DOWNLOAD['output'] = ""
    except subprocess.CalledProcessError as e:
        raise e
