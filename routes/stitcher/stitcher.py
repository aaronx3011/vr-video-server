
# Shell commands
import subprocess
import shlex
import threading

VIDEO = {'active': False, 'output': ''}

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