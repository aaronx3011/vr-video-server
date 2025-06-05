# Plafab
import playfab

# Utils 
import json

# PC interactions
import os
from dotenv import load_dotenv



load_dotenv(".env")

playfab.PlayFabSettings.TitleId = os.getenv("TitleId")
playfab.PlayFabSettings.DeveloperSecretKey = os.getenv("DeveloperSecretKey")
ACCOUNT_LINK_ID = os.getenv("ACCOUNT_LINK_ID")


StreamsDisponibles = {
        "Catalog": [],
        "Inventory": []
    }


def callback(success, failure):
    if success:
        pass
    else:
        print(failure)
 

def callback2(success, failure):
    if success:
        visibleItems = [ItemId["ItemId"] for ItemId in StreamsDisponibles["Inventory"]]
        for item in success["Catalog"]:
            if item["ItemId"] in visibleItems:
                StreamsDisponibles["Catalog"].append(item)
    else:
        print(failure)


def inventoryCallback(success, failure):

    if success:
        StreamsDisponibles["Inventory"] = success["Inventory"]
    else:
        print(failure)

loginRequest = {
    "CustomId": ACCOUNT_LINK_ID
}


def getInventory():
    login = playfab.PlayFabClientAPI.LoginWithCustomID(loginRequest, callback)
    result = playfab.PlayFabClientAPI.GetUserInventory(loginRequest, inventoryCallback)
    return json.dumps(StreamsDisponibles["Inventory"])


def GetItems():

    global StreamsDisponibles
    StreamsDisponibles = {
            "Catalog": [],
            "Inventory": []
        }
    getInventory()
    result = playfab.PlayFabClientAPI.GetCatalogItems({},callback2)
    return json.dumps(StreamsDisponibles["Catalog"])



def UpdateItem(item, status, SearchedTag):
    print(item, status, SearchedTag)
    if SearchedTag in item["Tags"]:
        request2 = {
            "Catalog":  
            [
                {
                    "ItemId": item.get("ItemId", None),
                    "CatalogVersion": item.get("CatalogVersion", None),
                    "DisplayName": status,
                    "ItemClass" : item.get("ItemClass", None),
                    "Description": item.get("Description", None),
                    "VirtualCurrencyPrices": item.get("VirtualCurrencyPrices", None),
                    "RealCurrencyPrices": item.get("RealCurrencyPrices", None),
                    "Tags": item.get("Tags", None),
                    "Consumable": item.get("Consumable", None),
                    "CanBecomeCharacter": item.get("CanBecomeCharacter", None),
                    "IsStackable": item.get("IsStackable", None),
                    "IsTradable": item.get("IsTradable", None),
                    "ItemImageUrl": item.get("ItemImageUrl", None),
                    "IsLimitedEdition": item.get("IsLimitedEdition", None),
                    "InitialLimitedEditionCount": item.get("InitialLimitedEditionCount", None)
                }
            ]
            
        }
        playfab.PlayFabAdminAPI.UpdateCatalogItems(request2, callback)
    
    return

def turnOnItems(SearchedTag):
    login = playfab.PlayFabClientAPI.LoginWithCustomID(loginRequest, callback)
    result = playfab.PlayFabClientAPI.GetUserInventory(
        loginRequest,
        lambda success,failure, tag=SearchedTag : [UpdateItem(i, "on", tag) for i in success["Inventory"]]
    )
    return



def turnOffItems(SearchedTag):
    login = playfab.PlayFabClientAPI.LoginWithCustomID(loginRequest,callback)
    result = playfab.PlayFabClientAPI.GetUserInventory(
        loginRequest,
        lambda success,failure, tag=SearchedTag : [UpdateItem(i, "off", tag) for i in success["Inventory"]]
    )
    return
