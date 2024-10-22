# Shell commands
import subprocess

def clearLocal():
    try:
        subprocess.check_call(['./videos/clearFolder.sh'])
    except subprocess.CalledProcessError as e:
        raise e