from rest_framework import serializers
from .models import Template
import json
from conduit.libs.registry import Registry
import os,subprocess,datetime
import requests

NEXUS_HTTP_URL = os.getenv('NEXUS_HTTP_URL', 'http://10.101.0.96:8081')
NEXUS_URL = os.getenv('NEXUS_URL', 'https://nexus.omef.cloud:5003')
NEXUS_USER = os.getenv('NEXUS_USER', 'openshift-deployer')
NEXUS_PASS= os.getenv('NEXUS_PASS', 'Openshift123!')
DOCKER_HUB_URL = os.getenv('DOCKER_HUB_URL', 'https://index.docker.io')
   
class TemplateSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Template
        fields = ('name', 'values','yaml','url','date_created', 'date_modified')
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
        if os.path.exists(helmScript):
            os.chmod(helmScript, 0o755)
            out = subprocess.Popen(str(helmScript)+' %s %s' % (str(app),str(chart),), 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT,shell=True)
            return out.communicate()
        else:
            print (str(helmScript) + ' does not exist')    

    def validate(self, data):
        """
        Check that start is before finish.
        """
        #jvalues = json.load(data['values'])
        if data['values'] is None :
            raise serializers.ValidationError("values must not be None")
        try:
            values = json.loads(str(data['values']))
            if values['chartName'] is None :
                raise serializers.ValidationError("values must not be None")
            if values['releaseName'] is None :
                raise serializers.ValidationError("values must not be None")
            r = Registry.create(NEXUS_URL, str(NEXUS_USER)+":"+str(NEXUS_PASS), False)
            registry = self.getImageRegistry(values)
            if registry is not None:
                values['image']['registry'] = registry
                with open(os.path.join(LIBS_PATH, "values.json"), 'w') as outfile:
                    json.dump(values, outfile)
            print(self.runHelmScript(os.path.join(LIBS_PATH, "helm.sh"),values['releaseName'],values['chartName']))
            if os.path.exists(os.path.join(LIBS_PATH, "out.yaml")) :
                timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                filename = values['releaseName'] + '_' + timestamp +'.yaml'
                os.rename(os.path.join(LIBS_PATH, "out.yaml"), os.path.join(LIBS_PATH, filename))
                r.uploadFile(NEXUS_HTTP_URL,os.path.join(LIBS_PATH, filename)) 
                nexus_url="{0}/repository/omef-raw-repo/yaml/{1}".format(NEXUS_URL[:-5],filename)
                print(nexus_url)
                data['valnexus_url'] = nexus_url
                data['values'] = None
            else:
                 serializers.ValidationError("Could not create template")   

        except Exception:
            raise serializers.ValidationError("Exception is happened:" + Exception.with_traceback)

        return data    