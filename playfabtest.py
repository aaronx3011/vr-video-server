import json
import playfab

# # Configura tu cliente PlayFab
playfab.PlayFabSettings.TitleId = "29E1D"
playfab.PlayFabSettings.DeveloperSecretKey = "O3GO7SA6S63CI3D9KOIN7KI7SCUM6TJBCM66TIQCBDIRNEN8OF"

# # Crea una solicitud para obtener el inventario global
# request = {
#     'CatalgoVersion': 'HLS1'
# }

StreamsDispnibles = {
        "Catalog": []
    }

def callback(success, failure):
    if success:
        pass
        print(success)
    else:
        pass
        print(failure)
 
# # Llama a la API para obtener el inventario global


# # Recorre los elementos del inventario global
# for item in result.catalog:
#     print(f"Nombre del item: {item.item_id}")
#     print(f"Descripción del item: {item.description}")


def callback2(success, failure):
    
    if success:
        # for item in success["Catalog"]:
        #     if (item["Tags"] != any):
        #         for i in item["Tags"]:
        #             StreamsDispnibles.append(i)
        # print(success)
        StreamsDispnibles["Catalog"] = success["Catalog"]
    else:
        print(failure)


# Crea una solicitud de inicio de sesión
request = {
    "Username": "alexander.tabata@vrinsitu.com",
    "Password": "Eroenckelman11.",
    "CustomId": "AF482D110F586149"
    }

# Llama a la API para iniciar sesión


def GetItems():
    login_result = playfab.PlayFabClientAPI.LoginWithCustomID(request,callback)
    result = playfab.PlayFabClientAPI.GetCatalogItems(request,callback2)
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
                    "ItemClass" : item.get("ItemId", None),
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
        #request = {'Catalog': [{'ItemId': 'BayernVsArsenal', 'ItemClass': '', 'CatalogVersion': 'HLS1', 'DisplayName': 'on', 'Description': '12:08:00', 'VirtualCurrencyPrices': {}, 'RealCurrencyPrices': {}, 'Tags': [], 'Consumable': {}, 'CanBecomeCharacter': False, 'IsStackable': False, 'IsTradable': False, 'ItemImageUrl': 'https://icdn.justarsenal.com/wp-content/uploads/2019/07/001.jpg', 'IsLimitedEdition': False, 'InitialLimitedEditionCount': 0}, {'ItemId': 'RealMadridVsManCity', 'ItemClass': '', 'CatalogVersion': 'HLS1', 'DisplayName': '', 'Description': '17:00', 'VirtualCurrencyPrices': {}, 'RealCurrencyPrices': {}, 'Tags': ['madrid', 'city', 'bigbuckbunnyclip', 'ism'], 'Consumable': {}, 'CanBecomeCharacter': False, 'IsStackable': False, 'IsTradable': False, 'ItemImageUrl': 'https://elcomercio.pe/resizer/tu2XnhHmZbYRERwR76LmiYqRtJ4=/787x442/smart/filters:format(jpeg):quality(75)/cloudfront-us-east-1.images.arcpublishing.com/elcomercio/USDNLPN7OJBQZF2J4NO4QX5UFY.jpg', 'IsLimitedEdition': False, 'InitialLimitedEditionCount': 0}, {'ItemId': 'BarcelonaVsP$G', 'ItemClass': '', 'CatalogVersion': 'HLS1', 'DisplayName': 'on', 'Description': '12:18:00', 'VirtualCurrencyPrices': {}, 'RealCurrencyPrices': {}, 'Tags': [], 'CustomData': '\n\n', 'Consumable': {}, 'CanBecomeCharacter': False, 'IsStackable': False, 'IsTradable': False, 'ItemImageUrl': 'https://i.pinimg.com/originals/9a/25/9c/9a259c45564fa7343c1396f43964b90d.png', 'IsLimitedEdition': False, 'InitialLimitedEditionCount': 0}, {'ItemId': 'Item_4', 'CatalogVersion': 'HLS1', 'DisplayName': 'on', 'VirtualCurrencyPrices': {}, 'RealCurrencyPrices': {}, 'Tags': [], 'Consumable': {}, 'CanBecomeCharacter': False, 'IsStackable': False, 'IsTradable': False, 'ItemImageUrl': 'https://vrinsitu-aaron-bucket.s3.amazonaws.com/imagenes/soccer8.png', 'IsLimitedEdition': False, 'InitialLimitedEditionCount': 0}, {'ItemId': 'item_5', 'CatalogVersion': 'HLS1', 'DisplayName': 'on', 'VirtualCurrencyPrices': {}, 'RealCurrencyPrices': {}, 'Tags': [], 'Consumable': {}, 'CanBecomeCharacter': False, 'IsStackable': False, 'IsTradable': False, 'ItemImageUrl': 'https://vrinsitu-aaron-bucket.s3.amazonaws.com/imagenes/soccer7.jpg', 'IsLimitedEdition': False, 'InitialLimitedEditionCount': 0}, {'ItemId': 'item_6', 'CatalogVersion': 'HLS1', 'DisplayName': 'on', 'VirtualCurrencyPrices': {}, 'RealCurrencyPrices': {}, 'Tags': [], 'Consumable': {}, 'CanBecomeCharacter': False, 'IsStackable': False, 'IsTradable': False, 'ItemImageUrl': 'https://vrinsitu-aaron-bucket.s3.amazonaws.com/imagenes/soccer4.jpg', 'IsLimitedEdition': False, 'InitialLimitedEditionCount': 0}]}
                #{'ItemId': 'item_6', 'CatalogVersion': 'HLS1', 'DisplayName': 'off', 'VirtualCurrencyPrices': {}, 'RealCurrencyPrices': {}, 'Tags': [], 'Consumable': {}, 'CanBecomeCharacter': False, 'IsStackable': False, 'IsTradable': False, 'ItemImageUrl': 'https://vrinsitu-aaron-bucket.s3.amazonaws.com/imagenes/soccer4.jpg', 'IsLimitedEdition': False, 'InitialLimitedEditionCount': 0}


        playfab.PlayFabAdminAPI.UpdateCatalogItems(request2, callback)
        

    
    return



# def callbackOn(success=any, failure=any, tag=''):
    
#     if success:
#         # print(success)
#         for item in success["Catalog"]:
#             # print(item["ItemId"])
#             # print(item["Tags"])
#             if tag in item["Tags"]:
#                 print()
#                 print(item["ItemId"])
#                 # UpdateItem(item["ItemId"], "off", "")

#     else:
#         print(failure)

def turnOnItems(SearchedTag):
    login_result = playfab.PlayFabClientAPI.LoginWithCustomID(request,callback)
    result = playfab.PlayFabClientAPI.GetCatalogItems(
        request,
        lambda success,failure, tag=SearchedTag : [UpdateItem(i, "on", tag) for i in success["Catalog"]]
    )
    return



def turnOffItems(SearchedTag):
    login_result = playfab.PlayFabClientAPI.LoginWithCustomID(request,callback)
    result = playfab.PlayFabClientAPI.GetCatalogItems(
        request,
        lambda success,failure, tag=SearchedTag : [UpdateItem(i, "off", tag) for i in success["Catalog"]]
    )
    return

# def GetItemsByTag():
#     login_result = playfab.PlayFabClientAPI.LoginWithCustomID(request,callback)
#     print("-------------------------------------- AQUI ------------------------------------")
#     result = playfab.PlayFabClientAPI.GetCatalogItems({"Filter": "Tags == madrid"},callback2)
#     return json.dumps(StreamsDispnibles["Catalog"])




# Ejemplo de uso

# print(GetItemsByTag())
# print("-------------------------------------- AQUI ------------------------------------")


# respaldo = {'Catalog' :[{'ItemId': 'BayernVsArsenal', 'CatalogVersion': 'HLS1', 'DisplayName': 'off', 'VirtualCurrencyPrices': {}, 'RealCurrencyPrices': {}, 'Tags': ['playlist', 'madrid', 'soteldo', 'disparochile'], 'Consumable': {}, 'CanBecomeCharacter': False, 'IsStackable': False, 'IsTradable': False, 'IsLimitedEdition': False, 'InitialLimitedEditionCount': 0}, {'ItemId': 'BarcelonaVsP$G', 'ItemClass': '', 'CatalogVersion': 'HLS1', 'DisplayName': 'on', 'Description': '12:18:00', 'VirtualCurrencyPrices': {}, 'RealCurrencyPrices': {}, 'Tags': [], 'CustomData': '\n\n', 'Consumable': {}, 'CanBecomeCharacter': False, 'IsStackable': False, 'IsTradable': False, 'ItemImageUrl': 'https://i.pinimg.com/originals/9a/25/9c/9a259c45564fa7343c1396f43964b90d.png', 'IsLimitedEdition': False, 'InitialLimitedEditionCount': 0}, {'ItemId': 'Item_4', 'CatalogVersion': 'HLS1', 'DisplayName': 'on', 'VirtualCurrencyPrices': {}, 'RealCurrencyPrices': {}, 'Tags': [], 'Consumable': {}, 'CanBecomeCharacter': False, 'IsStackable': False, 'IsTradable': False, 'ItemImageUrl': 'https://vrinsitu-aaron-bucket.s3.amazonaws.com/imagenes/soccer8.png', 'IsLimitedEdition': False, 'InitialLimitedEditionCount': 0}, {'ItemId': 'item_5', 'CatalogVersion': 'HLS1', 'DisplayName': 'on', 'VirtualCurrencyPrices': {}, 'RealCurrencyPrices': {}, 'Tags': [], 'Consumable': {}, 'CanBecomeCharacter': False, 'IsStackable': False, 'IsTradable': False, 'ItemImageUrl': 'https://vrinsitu-aaron-bucket.s3.amazonaws.com/imagenes/soccer7.jpg', 'IsLimitedEdition': False, 'InitialLimitedEditionCount': 0}, {'ItemId': 'item_6', 'CatalogVersion': 'HLS1', 'DisplayName': 'off', 'VirtualCurrencyPrices': {}, 'RealCurrencyPrices': {}, 'Tags': ['playlist', 'madrid', 'soteldo', 'disparochile'], 'Consumable': {}, 'CanBecomeCharacter': False, 'IsStackable': False, 'IsTradable': False, 'IsLimitedEdition': False, 'InitialLimitedEditionCount': 0}, {'ItemId': 'RealMadridVsManCity', 'CatalogVersion': 'HLS1', 'DisplayName': 'on', 'VirtualCurrencyPrices': {}, 'RealCurrencyPrices': {}, 'Tags': ['playlist', 'madrid', 'soteldo', 'disparochile'], 'Consumable': {}, 'CanBecomeCharacter': False, 'IsStackable': False, 'IsTradable': False, 'ItemImageUrl': 'https://ichef.bbci.co.uk/images/ic/640x360/p0fkzwny.jpg', 'IsLimitedEdition': False, 'InitialLimitedEditionCount': 0}]}

# playfab.PlayFabAdminAPI.UpdateCatalogItems(respaldo, callback)
# turnOnItems("madrid")

# print(StreamsDispnibles)

# print(GetItems())
# print("----------------------------------------- Aqui ----------------------------------------")
# UpdateItem("item_6", "off", "")
# print("----------------------------------------- Aqui ----------------------------------------")
# GetItems()
# print(GetItems())
# # Verifica si el inicio de sesión fue exitoso
# if login_result.success:
#     print("Inicio de sesión exitoso!")
#     # Ahora puedes realizar otras llamadas a la API
# else:
#     print("Error al iniciar sesión:", login_result.error)