from google.appengine.api import memcache
import os
import logging
import datetime
import simplejson as json
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError   
from google.appengine.ext.db import BadValueError
from google.appengine.runtime import DeadlineExceededError
from google.appengine.api import users
import hashlib
import logging

def create_md5_hexdigest(data):
	# Create MD5 Hexdigest
	md5 = hashlib.md5()
	md5.update(data)
	hexdigest = md5.hexdigest()
	return hexdigest

class BaseHandler(webapp.RequestHandler):

	context = {}
	now = None
	#ods_service_url = 'http://ec2-176-34-225-53.eu-west-1.compute.amazonaws.com:8080/kws/jaxrs/execute/o2/'
	ods_service_url = 'https://o2-poc-vital.razorfishsupport.com/kws/jaxrs/execute/o2/'
	service_request_headers = {
		'Content-Type':'application/xml'
	}
	def __init__(self):
		self.now = datetime.datetime.now()
		self.populateContext()
		
	def populateContext(self):

		self.context['now'] = self.now
		self.context['ods_service_url'] = self.ods_service_url
			
