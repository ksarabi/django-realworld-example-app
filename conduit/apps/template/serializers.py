from rest_framework import serializers
from .models import Template
import json
from conduit.libs.registry import Registry
import os,subprocess,datetime
import requests
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

NEXUS_HTTP_URL = os.getenv('NEXUS_HTTP_URL', 'http://10.101.0.96:8081')
NEXUS_URL = os.getenv('NEXUS_URL', 'https://nexus.omef.cloud:5003')
NEXUS_USER = os.getenv('NEXUS_USER', 'openshift-deployer')
NEXUS_PASS= os.getenv('NEXUS_PASS', 'Openshift123!')
DOCKER_HUB_URL = os.getenv('DOCKER_HUB_URL', 'https://index.docker.io')
LIBS_PATH = os.path.join(os.getcwd(),'conduit/libs')   
class TemplateSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Template
        fields = ('name', 'values','yaml','nexus_url','date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')

    def getImageRegistry(self,values):
        r = Registry.create(NEXUS_URL, NEXUS_USER+":"+NEXUS_PASS, False)
        if r.get_tag_digest(values['image']['repository'],values['image']['tag']) is not None :
            return NEXUS_URL[8:]
        rd = Registry.create(DOCKER_HUB_URL,None,False)    
        if rd.fetch_version(values['image']['repository'],values['image']['tag']) is not None :
            return DOCKER_HUB_URL[-9:] 
        return None    
    def runHelmScript(self,helmScript,app,chart):
        logger.error(str(helmScript) + ","+app+ ","+ chart) 
        if os.path.exists(helmScript):
            #os.chmod(helmScript, 0o755)
            try:
                #result = subprocess.check_output([helmScript,str(app),str(chart)], shell=True)
                result = subprocess.check_output(["{0} {1} {2}".format(helmScript,str(app),str(chart))], shell=True)
                #process = subprocess.Popen(["bash",str(helmScript),str(helmScript)[:-7],str(app),str(chart)], 
                #stdout=subprocess.PIPE, 
                #stderr=subprocess.STDOUT,shell=True)
                #output = process.stdout.read()
                #exitstatus = process.poll()
                #if (exitstatus==0):
                #        result = {"status": "Success", "output":str(output)}
                #else:
                #        result = {"status": "Failed", "output":str(output)}

            except Exception as e:
                    result =  {"status": "helm script is failed", "output":str(e.__cause__)}
                    raise serializers.ValidationError(result)
            return result
        else:
            logger.error(str(helmScript) + ' does not exist')    

    def validate(self, data):
        """
        Check that start is before finish.
        """
       
        try:
            if data['values'] is None :
                raise serializers.ValidationError("values must not be None")
            values = json.loads(str(data['values']))
            if values['chartName'] is None :
                raise serializers.ValidationError("values must not be None")
            result = values['chartName'].split('/')
            if len(result) != 2 or result[0] == '' or result[1] == '':
                raise serializers.ValidationError("invalid chartName")
            if values['releaseName'] is None :
                raise serializers.ValidationError("releaseName must not be None") 
            r = Registry.create(NEXUS_URL, str(NEXUS_USER)+":"+str(NEXUS_PASS), False)
            registry = self.getImageRegistry(values)
            if registry is not None:
                values['image']['registry'] = registry
                with open(os.path.join(LIBS_PATH, "values.json"), 'w') as outfile:
                    json.dump(values, outfile)
            else:
                raise serializers.ValidationError("could not find image with given tag,Invalid image or tag") 
            if values['commonLabels'] is None or values['image'].get('pullPolicy') is None or values['commonLabels'].get('version') is None:
                raise serializers.ValidationError("version or image.pullPolicy must not be None") 
            if values['image'].get('pullPolicy') != 'Always' and values['image'].get('pullPolicy') != 'IfNotPresent':
                raise serializers.ValidationError("image.pullPolicy must be either Always or IfNotPresent") 
            if values['service'] is None or values['service'].get('port') is None:
                raise serializers.ValidationError("service.port must not be None")             
            logger.error(self.runHelmScript(os.path.join(LIBS_PATH, "helm.sh"),values['releaseName'],values['chartName']))
            if os.path.exists(os.path.join(LIBS_PATH, "out.yaml")) :
                timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                filename = values['releaseName'] + '_' + timestamp +'.yaml'
                os.rename(os.path.join(LIBS_PATH, "out.yaml"), os.path.join(LIBS_PATH, filename))
                r.uploadFile(NEXUS_HTTP_URL,os.path.join(LIBS_PATH, filename)) 
                nexus_url="{0}/repository/omef-raw-repo/yaml/{1}".format(NEXUS_URL[:-5],filename)
                logger.error(nexus_url)
                data['nexus_url'] = nexus_url
            else:
                 logger.error("Could not create template")
                 raise serializers.ValidationError("Could not create yaml template") 
        except BaseException as error:
            print('An exception occurred: {}'.format(error.with_traceback))  
            raise serializers.ValidationError(error)         
        return data    