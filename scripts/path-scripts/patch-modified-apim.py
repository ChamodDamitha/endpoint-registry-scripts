from git import Repo
import os
import subprocess
from xml.dom import minidom
import shutil
import json

PREFIX = 'components/apimgt/'

def readConfig():
    with open('config.json', 'r') as f:
        data = f.read()

    return json.loads(data)


def extracyCarbonApimgtVersion(config):
    doc = minidom.parse(os.path.join(
        config['CARBON_APIMGT_LOCATION'], 'pom.xml'))
    return doc._get_firstChild()\
        .getElementsByTagName('properties')[0]\
        .getElementsByTagName('carbon.apimgt.version')[0]\
        .childNodes[0]\
        .nodeValue


def extractComponents(files):
    print('\nExtracting components...')
    components = set()
    for file in files:
        if file.startswith(PREFIX):
            component = file.replace(PREFIX, '').split('/')[0]
            components.add(component)
    print('Extracted components: ' + str([c for c in components]))
    return components


def filterIgnoredComponents(config, components):
    print('\nFiltering components...')
    ignoredComponents = config['IGNORED_COMPONENTS']
    print('Ignored components: ' + str(ignoredComponents))
    filteredComponents = [c for c in components if c not in ignoredComponents]
    print('Filtered componets: ' + str(filteredComponents))
    return filteredComponents


def buildComponents(config, components):
    print('\nBuilding components...')
    for c in components:
        COMPONENT_PATH = os.path.join(
            config['CARBON_APIMGT_LOCATION'], PREFIX, c)
        p = subprocess.Popen(['mvn', 'clean', 'install', '-Dmaven.test.skip=true'],
                             cwd=os.path.join(config['CARBON_APIMGT_LOCATION'],
                                              PREFIX, COMPONENT_PATH))
        p.wait()


def patchComponents(config, components, version):
    print('\nCopying built components...')
    for c in components:
        COMPONENT_TARGET_PATH = os.path.join(config['CARBON_APIMGT_LOCATION'],
                                             PREFIX, c, 'target')

        for f in os.listdir(COMPONENT_TARGET_PATH):
            source = os.path.join(COMPONENT_TARGET_PATH, f)
            if f == c + '-' + version + '.zip' \
                    or f == c + '-' + version + '.jar':
                # Copr new JAR/ZIP
                destination = os.path.join(
                    config['PATCH_DIR'], f.replace('-', '_', 1))
                shutil.copyfile(source, destination)
                print('Copied ' + source + ' to ' + destination + '\n')
            elif f.endswith('.war'):
                try:
                    # Deleted extracted WAR
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


config = readConfig()

repo = Repo(config['CARBON_APIMGT_LOCATION'])
assert not repo.bare

modifiedFiles = [item.a_path for item in repo.index.diff(None)]

components = extractComponents(modifiedFiles)

components = filterIgnoredComponents(config, components)

buildComponents(config, components)

carbonApimgtVersion = extracyCarbonApimgtVersion(config)

patchComponents(config, components, carbonApimgtVersion)
