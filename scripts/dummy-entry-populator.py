
from EndpointRegUtil import EndpointRegUtil
import random
import json


def execute():
    regPayload = {
        'name': 'WSO2 Dummy Registry ABC',
        'type': 'WSO2',
        'mode': 'READONLY'
    }
    reg = EndpointRegUtil.addRegistry(regPayload)
    if reg is None:
        return

    serviceTypes = ['REST', 'SOAP_1_1', 'GQL', 'WS']
    serviceCategories = ['UTILITY', 'EDGE', 'DOMAIN']
    definitionTypes = ['OAS', 'WSDL1', 'WSDL2', 'GQL_SDL']

    count = 0
    for i in range(20):
        definitionType = definitionTypes[random.randint(
            0, len(definitionTypes) - 1)]
        if definitionType == 'OAS':
            file = '../samples/swagger.json'
        elif definitionType == 'WSDL1' or definitionType == 'WSDL2':
            file = '../samples/wsdl1-sample.wsdl'
        else:
            file = '../samples/schema.graphql'

        entryPayload = {
            'entryName': 'Name' + str(random.randint(0, 100)),
            'serviceUrl': 'http://localhost/pizzashack',
            'serviceType': serviceTypes[random.randint(0, len(serviceTypes) - 1)],
            'serviceCategory': serviceCategories[random.randint(0, len(serviceCategories) - 1)],
            'definitionType': definitionType,
            'definitionUrl': 'https://petstore.swagger.io/v2/swagger.json',
            'metadata': '{ \'mutualTLS\' : true }'
        }

        entry = EndpointRegUtil.addRegistryEntry(reg['id'], entryPayload, file)
        if entry is not None:
            count += 1
    print("Entries added : " + str(count) + "/20")

    environment = {
        'name': 'dev-reg-only',
        'values': [
            {
                'key': 'regId',
                'value': reg['id'],
                'enabled': True
            }
        ]
    }

    with open('postman-environment-reg-only.json', 'w', encoding='utf-8') as f:
        json.dump(environment, f, ensure_ascii=False, indent=4)

    print('Done...!')


execute()
