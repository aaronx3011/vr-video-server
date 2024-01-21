import subprocess

proc = subprocess.Popen(
            [
                'nvidia-smi',
                '--query-gpu=utilization.gpu,utilization.memory,utilization.decoder,utilization.encoder',
                '--format=csv'

            ],
        )


