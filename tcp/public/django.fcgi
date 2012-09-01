#!/usr/bin/python

"""Specific for Alwaysdata fcgi hosting"""

from os import path
import os
import sys

_HERE = path.abspath(__file__)

_ROOT = path.dirname(path.dirname(path.dirname(path.dirname(_HERE))))
sys.path.insert(0, _ROOT)

# use virtualenv "venv" which is in the project's parent folder
activate_this = path.join(_ROOT, 'venv/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

_PROJECT_NAME = 'tcp'
os.environ['DJANGO_SETTINGS_MODULE'] = "%s.settings" % _PROJECT_NAME

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
