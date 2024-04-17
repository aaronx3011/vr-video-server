
import playfab

# # Configura tu cliente PlayFab
playfab.PlayFabSettings.TitleId = "29E1D"
# playfab.PlayFabSettings.developer_secret_key = "O3GO7SA6S63CI3D9KOIN7KI7SCUM6TJBCM66TIQCBDIRNEN8OF"

# # Crea una solicitud para obtener el inventario global
# request = {
#     'CatalgoVersion': 'HLS1'
# }

StreamsDispnibles = []

def callback(success, failure):
    if success:
        print(success)
    else:
        print(failure)
 
# # Llama a la API para obtener el inventario global


# # Recorre los elementos del inventario global
# for item in result.catalog:
#     print(f"Nombre del item: {item.item_id}")
#     print(f"Descripción del item: {item.description}")


def callback2(success, failure):
    for items in StreamsDispnibles:
        StreamsDispnibles.pop()
    
    if success:
        for item in success["Catalog"]:
            for i in item["Tags"]:
                StreamsDispnibles.append(i)
        # print(success)
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
    return StreamsDispnibles


# print(StreamsDispnibles)


# print(GetItems())
# # Verifica si el inicio de sesión fue exitoso
# if login_result.success:
#     print("Inicio de sesión exitoso!")
#     # Ahora puedes realizar otras llamadas a la API
# else:
#     print("Error al iniciar sesión:", login_result.error)