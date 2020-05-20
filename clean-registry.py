import requests

baseUrl = 'https://localhost:9443/api/am/endpoint-registry/v1/registries'

headers = {
    'Authorization': 'Basic YWRtaW46YWRtaW4='
}

# Retrieve all registries
response = requests.get(baseUrl, verify=False, headers=headers)
if (response.status_code == 200):
    registries = response.json()
    for reg in registries:
        # Delete the registry
        responseDelReg = requests.request("DELETE", baseUrl + "/" + reg["id"],
                                          verify=False,
                                          headers=headers)
        print(responseDelReg.text)
    print("Cleaned the registry")
else:
    print(response)
