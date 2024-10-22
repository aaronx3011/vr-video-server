# Shell commands
import subprocess
import shlex

def loopbackIsActive():
    try:
        process = subprocess.run("pactl list modules | grep module-loopback", shell= True, stdout= subprocess.PIPE)
        return process.stdout != b''
    except subprocess.CalledProcessError as e:
        raise e

def loopbackStart():
    try:
        subprocess.Popen(['pactl', 'load-module', 'module-loopback'], stdout=subprocess.PIPE).communicate()[0]
    except subprocess.CalledProcessError as e:
        raise e

    finally:
        return
        
def loopbackEnd():
    try:
        subprocess.Popen(['pactl', 'unload-module', 'module-loopback'], stdout=subprocess.PIPE).communicate()[0]
    except subprocess.CalledProcessError as e:
        raise e

    finally:
        return
