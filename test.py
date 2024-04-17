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
# aws_access_key_id = os.getenv("aws_access_key_id")
# aws_secret_access_key = os.getenv("aws_secret_access_key")

# print(aws_secret_access_key)



# import os
# from dotenv import load_dotenv

# load_dotenv('.env')

# Imprime las variables de entorno
# for key, value in os.environ.items():
#     print(f'{key}={value}')


# import os



# from dotenv import load_dotenv

# # Carga las variables del archivo .env
# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# load_dotenv(dotenv_path)

# # Accede a las variables
# aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
# aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# print (dotenv_path)

# import boto3

# session = boto3.Session(aws_access_key_id='AKIAVVIWKDRSJROFELGY',aws_secret_access_key='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')

# s3 = session.resource('s3')

# my_bucket = s3.Bucket('vrinsitu-aaron-bucket')



# for my_bucket_object in my_bucket.objects.all():
#     print(my_bucket_object.key)





# import os

# with open('test.txt', 'rb') as f:
#     try:  # catch OSError in case of a one line file 
#         f.seek(-2, os.SEEK_END)
#         while f.read(1) != b'\n':
#             f.seek(-2, os.SEEK_CUR)
#     except OSError:
#         f.seek(0)
#     last_line = f.readline().decode()


# print(last_line)




# i=0

# ids = [1,2,3,4,5]
# lista2 = []
# lista4 = []
# cont = len(ids)

# listw = [1,2,3,4,5,6,7,8,9]


# for id in ids:
#     if i <= 3:
#         lista4.append(id)
#     else:
#         break
#     i+= 1

# # for lista3 in lista:
# #     lista4.insert(lista3,prueba(lista3,1))

# print(lista4)

