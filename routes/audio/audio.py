# Shell commands
import subprocess

def alsaRecordDevices():
    try:
        devices = []
        proc = subprocess.Popen(
            ['arecord', '-l'],
            stdout=subprocess.PIPE).communicate()[0]

        lines = proc.decode("utf-8")[:-1].split("\n")

        for line in lines:
            if line.startswith("card "):
                devices.append({"name" : line, "index": line.split(":")[0].split(" ")[1]})
        
        return devices

    except subprocess.CalledProcessError as e:
        raise e
