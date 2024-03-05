# import subprocess

# proc = subprocess.Popen(
#             [
#                 'nvidia-smi',
#                 '--query-gpu=utilization.gpu,utilization.memory,utilization.decoder,utilization.encoder',
#                 '--format=csv'

#             ],
#         )

# proc = subprocess.Popen(['./server.sh'])


# import os
# from dotenv import load_dotenv

# load_dotenv()
# aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
# aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# print(aws_access_key_id)

import os



from dotenv import load_dotenv

# Carga las variables del archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Accede a las variables
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

print (dotenv_path)

