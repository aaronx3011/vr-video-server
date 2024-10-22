# Shell commands
import subprocess

def ffmpegInstalled() -> bool:
    try:
        subprocess.check_call(['ffmpeg', '-version'], stdout= subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        return False
    

def ffmpegVersion():
    try:
        proc = subprocess.Popen(['ffmpeg', '-version'], stdout=subprocess.PIPE).communicate()[0]
        return proc.decode("utf-8")[:-1].split("\n")

    except subprocess.CalledProcessError as e:
        raise e