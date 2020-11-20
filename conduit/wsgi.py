"""
WSGI config for conduit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conduit.settings")
NEXUS_HTTP_URL = os.getenv('NEXUS_HTTP_URL', 'http://10.101.0.96:8081')
NEXUS_URL = os.getenv('NEXUS_URL', 'https://nexus.omef.cloud:5003')
NEXUS_USER = os.getenv('NEXUS_USER', 'openshift-deployer')
NEXUS_PASS= os.getenv('NEXUS_PASS', 'Openshift123!')
DOCKER_HUB_URL = os.getenv('DOCKER_HUB_URL', 'https://index.docker.io')

application = get_wsgi_application()
