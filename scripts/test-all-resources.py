from EndpointRegUtil import EndpointRegUtil

createdRegistryIds = []


def test():
    # Add registries
    regPayload1 = {
        'name': 'Dummy Name 1',
        'type': 'WSO2',
        'mode': 'READONLY'
    }
    reg1 = EndpointRegUtil.addRegistry(regPayload1)
    if reg1 is None:
        print('Adding registry :' + regPayload1['name'] + ' failed')
        return
    createdRegistryIds.append(reg1['id'])

    regPayload2 = {
        'name': 'Dummy Name 2',
        'type': 'ETCD',
        'mode': 'READWRITE'
    }
    reg2 = EndpointRegUtil.addRegistry(regPayload2)
    if reg2 is None:
        print('Adding registry :' + regPayload2['name'] + ' failed')
        return
    createdRegistryIds.append(reg2['id'])
    print('Registries creation SUCCESS...!\n')

    # Get registries
    registries = EndpointRegUtil.getRegistries()
    regCount = 0
    for reg in registries:
        if reg['name'] == regPayload1['name']:
            regCount += 1
        if reg['name'] == regPayload2['name']:
            regCount += 1
        if regCount == 2:
            break
    if regCount != 2:
        print('Not all added registries not retrieved')
        return
    print('Registries retrieval SUCCESS...!\n')

    # Get registry
    reg = EndpointRegUtil.getRegistry(reg1['id'])
    if reg is None:
        print('Getting registry: ' + reg1['name'] + ' failed')
        return
    print('Registry retrieval SUCCESS...!\n')

    # Update registry
    regPayload1New = {
        'name': 'Dummy Name 1 Updated',
        'type': 'WSO2',
        'mode': 'READONLY'
    }
    regUpdated = EndpointRegUtil.updateRegistry(reg['id'], regPayload1New)
    if regUpdated is None or regUpdated['name'] != regPayload1New['name']:
        print(regUpdated)
        print('Updating registry :' + reg['name'] + ' failed')
        return
    print('Registry update SUCCESS...!\n')

    # Add entry
    file1 = '../samples/swagger.json'
    entryPayload1 = {
        'entryName': 'Dummy Entry Name 1',
        'serviceUrl': 'http://localhost/pizzashack',
        'serviceType': 'SOAP_1_1',
        'serviceCategory': 'UTILITY',
        'definitionType': 'OAS',
        'definitionUrl': 'https://petstore.swagger.io/v2/swagger.json',
        'metadata': '{ \'mutualTLS\' : true }'
    }
    entry1 = EndpointRegUtil.addRegistryEntry(reg['id'], entryPayload1, file1)
    if entry1 is None:
        print('Adding registry entry: ' +
              entryPayload1['entryName'] + ' failed')
        return

    file2 = '../samples/swagger.json'
    entryPayload2 = {
        'entryName': 'Dummy Entry Name 2',
        'serviceUrl': 'http://localhost/pizzashack',
        'serviceType': 'REST',
        'serviceCategory': 'DOMAIN',
        'definitionType': 'OAS',
        'definitionUrl': 'https://petstore.swagger.io/v2/swagger.json',
        'metadata': '{ \'mutualTLS\' : true }'
    }
    entry2 = EndpointRegUtil.addRegistryEntry(reg['id'], entryPayload2, file2)
    if entry2 is None:
        print('Adding registry entry: ' +
              entryPayload2['entryName'] + ' failed')
        return
    print('Entries creation SUCCESS...!\n')

    # Get entries
    entries = EndpointRegUtil.getRegistryEntries(reg['id'])
    entryCount = 0
    for entry in entries:
        if entry['entryName'] == entryPayload1['entryName']:
            entryCount += 1
        if entry['entryName'] == entryPayload2['entryName']:
            entryCount += 1
        if entryCount == 2:
            break
    if entryCount != 2:
        print('Not all added registry entries not retrieved')
        return
    print('Entries retrieval SUCCESS...!\n')

    # Get entry
    entry = EndpointRegUtil.getRegistryEntry(reg['id'], entry1['id'])
    if entry is None:
        print('Getting registry entry: ' + entry1['entryName'] + ' failed')
        return
    print('Entry retrieval SUCCESS...!\n')

    # Update entry
    file1New = '../samples/swagger.json'
    entryPayload1New = {
        'entryName': 'Dummy Entry Name 1 Updated',
        'serviceUrl': 'http://localhost/pizzashack',
        'serviceType': 'SOAP_1_1',
        'serviceCategory': 'UTILITY',
        'definitionType': 'OAS',
        'definitionUrl': 'https://petstore.swagger.io/v2/swagger.json',
        'metadata': '{ \'mutualTLS\' : true }'
    }
    entryUpdated = EndpointRegUtil.updateRegistryEntry(reg['id'], entry['id'],
                                                       entryPayload1New,
                                                       file1New)
    if entryUpdated is None or entryUpdated['entryName'] != entryPayload1New['entryName']:
        print('Updating registry entry: ' +
              entryPayload1New['entryName'] + ' failed')
        return
    print('Entry update SUCCESS...!\n')

    # Delete entry
    entryDeleted = EndpointRegUtil.deleteRegistryEntry(reg['id'], entry['id'])
    if not entryDeleted:
        print('Deleting registry entry: ' + entry['entryName'] + ' failed')
        return
    print('Entry deletion SUCCESS...!\n')

    # Delete registry
    regDeleted = EndpointRegUtil.deleteRegistry(reg['id'])
    if not regDeleted:
        print('Deleting registry : ' + reg['name'] + ' failed')
        return
    createdRegistryIds.remove(reg['id'])
    print('Registry deletion SUCCESS...!\n')

    print('All tests passed....!\n\n')
    return


def cleanUp():
    allCleaned = True
    for regId in createdRegistryIds:
        deleted = EndpointRegUtil.deleteRegistry(regId)
        if not deleted:
            print('Removing registry with id: ' + regId + ' failed')
            allCleaned = False
    if allCleaned:
        print('Created registries/entries are removed...!')


test()
cleanUp()
