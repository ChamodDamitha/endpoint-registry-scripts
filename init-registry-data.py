import requests
import json
import os
import random

baseUrl = 'https://localhost:9443/api/am/endpoint-registry/v1/registries'

regAdded = False
entryAdded = False

# Add registry
regHeaders = {
    'Authorization': 'Basic YWRtaW46YWRtaW4=',
    'Content-Type': 'application/json'
}
for i in range(20):
    regPayload = {
        'name': 'WSO2 Dev Registry ' + str(random.randint(0, 100)),
        'type': 'WSO2',
        'mode': 'READONLY'
    }
    responseAddReg = requests.post(
        baseUrl, verify=False, headers=regHeaders, data=json.dumps(regPayload))
    if (responseAddReg.status_code != 200):
        continue
    reg = responseAddReg.json()
    print(reg)
    regAdded = True
    break

# Add entry
if regAdded:
    entryHeaders = {
        'Authorization': 'Basic YWRtaW46YWRtaW4=',
        'Content-Type': 'multipart/form-data'
    }
    file = 'samples/swagger.json'
    for i in range(20):
        entryPayload = {
            'entryName': 'Pizzashack-Endpoint ' + str(random.randint(0, 100)),
            'serviceUrl': 'http://localhost/pizzashack',
            'serviceType': 'SOAP_1_1',
            'serviceCategory': 'UTILITY',
            'definitionType': 'OAS',
            'definitionUrl': 'https://petstore.swagger.io/v2/swagger.json',
            'metadata': '{ \'mutualTLS\' : true }'
        }
        files = {
            'registryEntry': (None, json.dumps(entryPayload),
                              'application/json'),
            'definitionFile': (os.path.basename(file), open(file, 'rb'),
                               'application/octet-stream')
        }

        responseAddEntry = requests.post(baseUrl + '/' + reg['id'] + '/entry',
                                         verify=False,
                                         headers=entryHeaders,
                                         files=files
                                         )
        if responseAddEntry.status_code != 200:
            continue
        entry = responseAddEntry.json()
        print(entry)
        entryAdded = True
        break

# Delete registry
if regAdded and ~entryAdded:
    deleteRegHeaders = {'Authorization': 'Basic YWRtaW46YWRtaW4='}
    responseDelReg = requests.request("DELETE", baseUrl, verify=False,
                                      headers=deleteRegHeaders)
    print(responseAddReg.text)

# Dump postman environment file
if regAdded and entryAdded:
    environment = {
        'name': 'dev',
        'values': [
            {
                'key': 'regId',
                'value': reg['id'],
                'enabled': True
            },
            {
                'key': 'entryId',
                'value': entry['id'],
                'enabled': True
            }
        ]
    }

    with open('postman-environment.json', 'w', encoding='utf-8') as f:
        json.dump(environment, f, ensure_ascii=False, indent=4)
else:
    print("No record added")
