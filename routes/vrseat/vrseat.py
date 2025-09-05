# Network interactions
import requests

# Utils 
import json

# PC interactions
import os
from dotenv import load_dotenv



load_dotenv(".env")


API_URL = str(os.getenv("VRSEAT_API_URL"))
AUTH_TOKEN = str(os.getenv("VRSEAT_AUTH_TOKEN"))


def getInventory():

    response = requests.get(
        API_URL,
        headers= {'Authorization': f"Bearer {AUTH_TOKEN}"}
    )
    print(AUTH_TOKEN)
    
    print(response.json())

    return response.json()



def modifyItem(itemId:str, status:str="not-defined"):
    try:
        response = requests.put(
            f"{API_URL}{itemId}",
            headers= {'Authorization': f"Bearer {AUTH_TOKEN}"},
            data= {'status': status}

        )
        return response
    except Exception as e:
        print(e)


def turnOnItems(itemId):
    modifyItem(itemId, 'active')

def turnOffItems(itemId):
    modifyItem(itemId, 'off')


