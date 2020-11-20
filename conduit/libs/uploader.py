import os,re
import requests
import json

#NEXUS_URL = os.getenv('NEXUS_URL', 'https://nexus.omef.cloud:5003')
NEXUS_HTTP_URL = os.getenv('NEXUS_URL', 'http://10.101.0.96:8081')
NEXUS_USER = os.getenv('NEXUS_USER', 'openshift-deployer')
NEXUS_PASS= os.getenv('NEXUS_PASS', 'Openshift123!')
DOCKER_HUB_URL = os.getenv('DOCKER_HUB_URL', 'https://index.docker.io')
#DOCKER_HUB_URL = os.getenv('DOCKER_HUB_URL', 'https://hub.docker.com')

def uploadFile(path,username,password):
    filename = os.path.basename(path)
    files = {
        'raw.directory': (None, '/yaml/'),  # folder structure you want in nexus
        'raw.asset1': (open(path, 'rb')),
        'raw.asset1.filename': (None, filename),  # this is the name you want to see in nexus
    }
    print (files)
    response = requests.post('{0}/service/rest/v1/components?repository=omef-raw-repo'.format(NEXUS_HTTP_URL), files=files,auth=(username, password),verify=False)
    return response

#filename = 'values.json'
#with open(filename) as f:
#  values = json.load(f)

print(uploadFile('out.yaml','api-user','ManTechOMEF123!'))