import json
import random
from EndpointRegUtil import EndpointRegUtil

regAdded = False
entryAdded = False

# Add registry
for i in range(20):
    regPayload = {
        'name': 'WSO2 Dev Registry ' + str(random.randint(0, 100)),
        'type': 'WSO2',
        'mode': 'READONLY'
    }
    reg = EndpointRegUtil.addRegistry(regPayload)
    if reg is not None:
        regAdded = True
        break

# Add entry
if regAdded:
    file = '../samples/swagger.json'
    for i in range(20):
        payload = {
            'entryName': 'Pizzashack-Endpoint ' + str(random.randint(0, 100)),
            'serviceUrl': 'http://localhost/pizzashack',
            'serviceType': 'SOAP_1_1',
            'serviceCategory': 'UTILITY',
            'definitionType': 'OAS',
            'definitionUrl': 'https://petstore.swagger.io/v2/swagger.json',
            'metadata': '{ \'mutualTLS\' : true }'
        }

        entry = EndpointRegUtil.addRegistryEntry(reg['id'],
                                                 payload, file)
        if entry is not None:
            entryAdded = True
            break
        print(entry)

# Delete registry
if regAdded and not entryAdded:
    EndpointRegUtil.deleteRegistry(reg['id'])

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
    print('No record added')
