import json
import playfab

playfab.PlayFabSettings.TitleId = "29E1D"
playfab.PlayFabSettings.DeveloperSecretKey = "O3GO7SA6S63CI3D9KOIN7KI7SCUM6TJBCM66TIQCBDIRNEN8OF"

ACCOUNT_LINK_ID = "548E91C355E6FAB2"


StreamsDispnibles = {
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
        visibleItems = [ItemId["ItemId"] for ItemId in StreamsDispnibles["Inventory"]]
        for item in success["Catalog"]:
            if item["ItemId"] in visibleItems:
                StreamsDispnibles["Catalog"].append(item)
    else:
        print(failure)


def inventoryCallback(success, failure):
    
    if success:
        StreamsDispnibles["Inventory"] = success["Inventory"]
    else:
        print(failure)

loginRequest = {
    "CustomId": ACCOUNT_LINK_ID
}


def getInventory():
    login = playfab.PlayFabClientAPI.LoginWithCustomID(loginRequest, callback)
    result = playfab.PlayFabClientAPI.GetUserInventory(loginRequest, inventoryCallback)
    return json.dumps(StreamsDispnibles["Inventory"])


def GetItems():
    getInventory()
    result = playfab.PlayFabClientAPI.GetCatalogItems({},callback2)
    return json.dumps(StreamsDispnibles["Catalog"])



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