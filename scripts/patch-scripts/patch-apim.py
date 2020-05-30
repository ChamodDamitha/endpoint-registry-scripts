import os
import subprocess
from xml.dom import minidom
import shutil
import json
import sys

PREFIX = 'components/apimgt/'


def readConfig(configPath):
    with open(configPath, 'r') as f:
        data = f.read()
    return json.loads(data)


def extractCarbonApimgtVersion(config):
    doc = minidom.parse(os.path.join(
        config['CARBON_APIMGT_LOCATION'], 'pom.xml'))
    return doc._get_firstChild()\
        .getElementsByTagName('properties')[0]\
        .getElementsByTagName('carbon.apimgt.version')[0]\
        .childNodes[0]\
        .nodeValue


def extractModifiedComponent(file):
    print('\nExtracting modified component...')
    for subPath in file.split('/'):
        if 'org.wso2' in subPath:
            return subPath
    return None


def buildComponent(config, component):
    print('\nBuilding component...')
    COMPONENT_PATH = os.path.join(
        config['CARBON_APIMGT_LOCATION'], PREFIX, component)
    p = subprocess.Popen(['mvn', 'clean', 'install', '-Dmaven.test.skip=true'],
                         cwd=os.path.join(config['CARBON_APIMGT_LOCATION'],
                                          PREFIX, COMPONENT_PATH),
                         stdout=subprocess.PIPE)
    status = False
    while True:
        output = p.stdout.readline()
        if output:
            print(output)
            if not status and b'BUILD SUCCESS' in output:
                status = True
        if p.poll() is not None:
            break

    if status:
        print('\nSuccesfully built <' + component + '>\n')
    else:
        print('\nFailed to build <' + component + '>\n')
    return status


def patchComponent(config, component, version):
    print('\nPatching built component...')
    COMPONENT_TARGET_PATH = os.path.join(config['CARBON_APIMGT_LOCATION'],
                                         PREFIX, component, 'target')

    for f in os.listdir(COMPONENT_TARGET_PATH):
        source = os.path.join(COMPONENT_TARGET_PATH, f)
        if f == component + '-' + version + '.zip' \
                or f == component + '-' + version + '.jar':
            # Copy new JAR/ZIP
            destination = os.path.join(
                config['PATCH_DIR'], f.replace('-', '_', 1))
            try:
                shutil.copyfile(source, destination)
            except FileNotFoundError:
                os.mkdir(config['PATCH_DIR'])
                shutil.copyfile(source, destination)
            print('Copied ' + source + ' to ' + destination + '\n')
        elif f.endswith('.war'):
            try:
                # Delete extracted WAR
                extractedWar = os.path.join(
                    config['WEB_APP_DIR'], f.replace('.war', ''))
                shutil.rmtree(extractedWar)
                print('Deleted ' + extractedWar + '\n')
            except FileNotFoundError:
                pass
            # Copy new WAR
            destination = os.path.join(config['WEB_APP_DIR'], f)
            shutil.copyfile(source, destination)
            print('Copied ' + source + ' to ' + destination + '\n')


def run(configPath, modifiedFilePath):
    config = readConfig(configPath)
    carbonApimgtVersion = extractCarbonApimgtVersion(config)
    if not carbonApimgtVersion:
        print('Failed to detect carbon.apimgt.version')
        return
    print('carbon.apimgt.version: ' + carbonApimgtVersion)

    component = extractModifiedComponent(modifiedFilePath)
    if not component:
        print('Modified Component extraction failed')
        return
    print('\n Component: ' + component)

    buildStatus = buildComponent(config, component)
    if not buildStatus:
        return

    patchComponent(config, component, carbonApimgtVersion)


run(sys.argv[1], sys.argv[2])
