import requests
import json
import os


class EndpointRegUtil:
    BASIC_AUTH_CREDENTIALS = "YWRtaW46YWRtaW4="
    BASE_URL = 'https://localhost:9443/api/am/endpoint-registry/v1/registries'

    @staticmethod
    def getRegistries():
        headers = {
            'Authorization': 'Basic ' + EndpointRegUtil.BASIC_AUTH_CREDENTIALS
        }
        response = requests.get(EndpointRegUtil().BASE_URL, verify=False,
                                headers=headers)
        if (response.status_code == 200):
            return response.json()
        print(response.text)
        return {}

    @staticmethod
    def addRegistry(payload):
        headers = {
            'Authorization': 'Basic ' + EndpointRegUtil.BASIC_AUTH_CREDENTIALS,
            'Content-Type': 'application/json'
        }
        response = requests.post(
            EndpointRegUtil().BASE_URL, verify=False, headers=headers,
            data=json.dumps(payload))
        print(response.text)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def deleteRegistry(regId):
        headers = {
            'Authorization': 'Basic ' + EndpointRegUtil.BASIC_AUTH_CREDENTIALS
        }
        response = requests.request("DELETE", EndpointRegUtil().BASE_URL + "/"
                                    + regId, verify=False, headers=headers)
        print(response.text)
        return response.status_code == 200

    @staticmethod
    def addRegistryEntry(regId, payload, file):
        headers = {
            'Authorization': 'Basic ' + EndpointRegUtil.BASIC_AUTH_CREDENTIALS,
            'Content-Type': 'multipart/form-data'
        }
        files = {
            'registryEntry': (None, json.dumps(payload),
                              'application/json'),
            'definitionFile': (os.path.basename(file), open(file, 'rb'),
                               'application/octet-stream')
        }

        response = requests.post(EndpointRegUtil.BASE_URL + '/' + regId
                                 + '/entry',
                                 verify=False,
                                 headers=headers,
                                 files=files
                                 )
        print(response.text)
        if response.status_code == 200:
            return response.json()
        return None
