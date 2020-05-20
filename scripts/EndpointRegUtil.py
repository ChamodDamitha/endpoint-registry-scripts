import requests
import json
import os


class EndpointRegUtil:
    BASIC_AUTH_CREDENTIALS = 'YWRtaW46YWRtaW4='
    BASE_URL = 'https://localhost:9443/api/am/endpoint-registry/v1/registries'

# Registry resources
    @staticmethod
    def getRegistries():
        headers = {
            'Authorization': 'Basic ' + EndpointRegUtil.BASIC_AUTH_CREDENTIALS
        }
        response = requests.get(EndpointRegUtil.BASE_URL, verify=False,
                                headers=headers)
        if (response.status_code == 200):
            return response.json()
        print(response.text)
        return {}

    @staticmethod
    def getRegistry(regId):
        headers = {
            'Authorization': 'Basic ' + EndpointRegUtil.BASIC_AUTH_CREDENTIALS
        }
        response = requests.get(EndpointRegUtil.BASE_URL + '/' + regId,
                                verify=False,
                                headers=headers)
        if (response.status_code == 200):
            return response.json()
        print(response.text)
        return None

    @staticmethod
    def addRegistry(payload):
        headers = {
            'Authorization': 'Basic ' + EndpointRegUtil.BASIC_AUTH_CREDENTIALS,
            'Content-Type': 'application/json'
        }
        response = requests.post(
            EndpointRegUtil.BASE_URL, verify=False, headers=headers,
            data=json.dumps(payload))
        print(response.text)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def updateRegistry(regId, payload):
        headers = {
            'Authorization': 'Basic ' + EndpointRegUtil.BASIC_AUTH_CREDENTIALS,
            'Content-Type': 'application/json'
        }

        response = requests.request('PUT', EndpointRegUtil.BASE_URL + '/'
                                    + regId, verify=False, headers=headers,
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
        response = requests.request('DELETE', EndpointRegUtil.BASE_URL + '/'
                                    + regId, verify=False, headers=headers)
        print(response.text)
        return response.status_code == 200

# Registry Entry resources
    @staticmethod
    def getRegistryEntries(regId):
        headers = {
            'Authorization': 'Basic ' + EndpointRegUtil.BASIC_AUTH_CREDENTIALS
        }
        response = requests.get(EndpointRegUtil.BASE_URL
                                + '/' + regId + '/entries',
                                verify=False,
                                headers=headers)
        if (response.status_code == 200):
            return response.json()
        print(response.text)
        return {}

    @staticmethod
    def getRegistryEntry(regId, entryId):
        headers = {
            'Authorization': 'Basic ' + EndpointRegUtil.BASIC_AUTH_CREDENTIALS
        }
        response = requests.get(EndpointRegUtil.BASE_URL
                                + '/' + regId + '/entries/' + entryId,
                                verify=False,
                                headers=headers)
        if (response.status_code == 200):
            return response.json()
        print(response.text)
        return None

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

    @staticmethod
    def updateRegistryEntry(regId, entryId, payload, file):
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

        response = requests.request('PUT',
                                    EndpointRegUtil.BASE_URL + '/' + regId +
                                    '/entries/' + entryId,
                                    verify=False,
                                    headers=headers,
                                    files=files)
        print(response.text)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def deleteRegistryEntry(regId, entryId):
        headers = {
            'Authorization': 'Basic ' + EndpointRegUtil.BASIC_AUTH_CREDENTIALS
        }
        response = requests.request('DELETE',
                                    EndpointRegUtil.BASE_URL + '/' + regId +
                                    '/entries/' + entryId,
                                    verify=False,
                                    headers=headers)
        print(response.text)
        return response.status_code == 200
