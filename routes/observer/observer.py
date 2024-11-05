# Shell commands
import subprocess
import threading

# Constants
OBSERVER = {'active': False, 'output': ''}


def observerStartCommand():
    try:
        process = subprocess.Popen(
            ['./videos/observer.sh'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        for line in process.stdout:
            OBSERVER["output"] = line[:-1]
        OBSERVER["active"] = False
        OBSERVER["output"] = ""
    except subprocess.CalledProcessError as e:
        raise e
    return True

def observerStart():
    try:
        if OBSERVER['active'] == False:
            x = threading.Thread(target=observerStartCommand)
            x.start()
            OBSERVER['active'] = True
        else:
            e = subprocess.CalledProcessError(999, "", "This process is already running", "This process is already running")
            raise e

    except subprocess.CalledProcessError as e:
        raise e

def observerStop():
    try:
        subprocess.check_call(['pkill', 'inotify'], stdout= subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise e