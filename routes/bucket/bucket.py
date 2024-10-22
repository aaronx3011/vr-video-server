# Utils
import time

# Shell commands
import subprocess
import shlex

AWS = {"active": False, "output" : ""}

def clearFilesByNameRecursive(folder, fileName):
    try:
        command = f"aws s3 rm s3://vrinsitu-aaron-bucket/{folder} --exclude '*' --include '*{fileName}*' --recursive"
        subprocess.Popen(
            shlex.split(command),
            stdout=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        raise e

def clearFilesByName(folder, fileName):
    try:
        command = f"aws s3 rm s3://vrinsitu-aaron-bucket/{folder} --exclude '*' --include '*{fileName}*'"
        subprocess.Popen(
            shlex.split(command),
            stdout=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        raise e

def syncFromLocalFolderToAWS(folder):
    try:
        command = f"aws s3 sync ./{folder} s3://vrinsitu-aaron-bucket/{folder}" 
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
            command = f"aws s3 sync s3://vrinsitu-aaron-bucket/{folder} s3://vrinsitu-aaron-bucket/{folder}{time.time()}" 
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