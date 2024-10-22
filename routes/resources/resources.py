# PC interactions
import psutil

# Shell commands
import subprocess

def utilization():
    try:
        proc = subprocess.Popen(
            [
                'nvidia-smi',
                '--query-gpu=utilization.gpu,utilization.memory,utilization.decoder,utilization.encoder',
                '--format=csv'
            ],
            stdout=subprocess.PIPE
        ).communicate()[0]

        keys = proc.decode("utf-8")[:-1].split("\n")[0].split(", ")
        values = proc.decode("utf-8")[:-1].split("\n")[1].split(", ")
        usage = {
            "utilization.cpu [%]" : psutil.cpu_percent(),
            "utilization.ram [%]" : psutil.virtual_memory().percent
            }
        
        i= 0
        for key in keys:
            usage[key] = float(values[i][:-2])
            i += 1

        return usage

    except subprocess.CalledProcessError as e:
        raise e