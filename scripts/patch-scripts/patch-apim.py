from git import Repo
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


def extracyCarbonApimgtVersion(config):
    doc = minidom.parse(os.path.join(
        config['CARBON_APIMGT_LOCATION'], 'pom.xml'))
    return doc._get_firstChild()\
        .getElementsByTagName('properties')[0]\
        .getElementsByTagName('carbon.apimgt.version')[0]\
        .childNodes[0]\
        .nodeValue


def extractModifiedComponents(files):
    print('\nExtracting modified components...')
    components = set()
    for file in files:
        if file.startswith(PREFIX):
            component = file.replace(PREFIX, '').split('/')[0]
            components.add(component)
    print('Modified components: ' + str([c for c in components]))
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
            print('\nSuccesfully built <' + c + '>\n')
        else:
            print('\nFailed to build <' + c + '>\n')
            return False
    return True


def patchComponents(config, components, version):
    print('\nPatching built components...')
    for c in components:
        COMPONENT_TARGET_PATH = os.path.join(config['CARBON_APIMGT_LOCATION'],
                                             PREFIX, c, 'target')

        for f in os.listdir(COMPONENT_TARGET_PATH):
            source = os.path.join(COMPONENT_TARGET_PATH, f)
            if f == c + '-' + version + '.zip' \
                    or f == c + '-' + version + '.jar':
                # Copy new JAR/ZIP
                destination = os.path.join(
                    config['PATCH_DIR'], f.replace('-', '_', 1))
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


def run(configPath):
    config = readConfig(configPath)
    carbonApimgtVersion = extracyCarbonApimgtVersion(config)
    if not carbonApimgtVersion:
        print('Failed to detect carbon.apimgt.version')
        return
    print('carbon.apimgt.version: ' + carbonApimgtVersion)

    repo = Repo(config['CARBON_APIMGT_LOCATION'])
    assert not repo.bare

    modifiedFiles = [item.a_path for item in repo.index.diff(None)]
    if not modifiedFiles:
        print('No modified files')
        return

    components = extractModifiedComponents(modifiedFiles)
    if not components:
        print('Modified Component extraction failed')
        return

    components = filterIgnoredComponents(config, components)
    if not components:
        print('No Components after filtering ignored components')
        return

    buildStatus = buildComponents(config, components)
    if not buildStatus:
        return

    patchComponents(config, components, carbonApimgtVersion)


run(sys.argv[1])
