import os,subprocess,datetime
import requests
import json
from registry import Registry

NEXUS_HTTP_URL = os.getenv('NEXUS_HTTP_URL', 'http://10.101.0.96:8081')
NEXUS_URL = os.getenv('NEXUS_URL', 'https://nexus.omef.cloud:5003')
NEXUS_USER = os.getenv('NEXUS_USER', 'openshift-deployer')
NEXUS_PASS= os.getenv('NEXUS_PASS', 'Openshift123!')
DOCKER_HUB_URL = os.getenv('DOCKER_HUB_URL', 'https://index.docker.io')



filename = 'values.json'
with open(filename) as f:
  values = json.load(f)

def getImageRegistry(values):
    r = Registry.create(NEXUS_URL, NEXUS_USER+":"+NEXUS_PASS, False)
    if r.get_tag_digest(values['image']['repository'],values['image']['tag']) is not None :
        return NEXUS_URL[8:]
    rd = Registry.create(DOCKER_HUB_URL,None,False)    
    if rd.fetch_version(values['image']['repository'],values['image']['tag']) is not None :
        return DOCKER_HUB_URL[-9:] 
    return None    
def runHelmScript(helmScript,app,chart):
    if os.path.exists(helmScript):
      os.chmod(helmScript, 0o755)
      out = subprocess.Popen(str(helmScript)+' %s %s' % (str(app),str(chart),), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,shell=True)
      return out.communicate()
    else:
      print (str(helmScript) + ' does not exist')  

r = Registry.create(NEXUS_URL, "ksarabi:ManTechOMEF123!", False)
registry = getImageRegistry(values)
if registry is not None:
  values['image']['registry'] = registry
  with open('values.json', 'w') as outfile:
    json.dump(values, outfile)
print(runHelmScript(values['releaseName'],values['chartName']))
if os.path.exists("out.yaml") :
  timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  filename = values['releaseName'] + '_' + timestamp +'.yaml'
  os.rename('out.yaml', filename)
  r.uploadFile(NEXUS_HTTP_URL,filename) 
  nexus_url="{0}/repository/omef-raw-repo/yaml/{1}".format(NEXUS_URL[:-5],filename)
  print(nexus_url)