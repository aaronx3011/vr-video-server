# UDP interactions
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def connectToGoogle(skt):
    try:
        return skt.connect(("8.8.8.8", 80))
    except Exception as e:
        raise e

def getLocalIPv4():
    try:
        connectToGoogle(s)
        localIPv4 = s.getsockname()[0]
        endConnection(s)
        return localIPv4
    except Exception as e:
        raise e

def endConnection(skt):
    try:
        skt.close()
    except Exception as e:
        raise e