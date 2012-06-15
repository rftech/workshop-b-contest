	from google.appengine.ext import webapp
import os
import datetime
import logging
from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
from operator import itemgetter
from google.appengine.api import memcache

# Import local scripts
from controllers import utils


"""
	@description:
		This handler makes requests to the ODS end point
		The response will be raw feed data

"""
class ServiceAHandler(utils.BaseHandler):
	def get(self):
		taskqueue.add(queue_name='service', url='/tasks/service-a', method='POST', payload='', countdown=0)

		# Return the request
		self.redirect('/')
		return

	def post(self):
		response = None
		payload = None
		json_response = None
		url = ''
		try:
			logging.debug('ServiceAHandler() : post() : Running Task')
			
			# Create the XML Request string
			payload = prepareServiceAHandlerURL()

			logging.debug(payload)

			url = self.ods_service_url + '/techsummit/service-a.robot'

			response = urlfetch.fetch(url, 
				payload=payload, 
				method='POST', 
				headers=self.service_request_headers, 
				allow_truncated=False, 
				follow_redirects=False, 
				deadline=60, 
				validate_certificate=False
			)
			
			logging.debug(response)
			if response.status_code == 200:
				memcache.set(key='service_a_data:raw', value=response.content)
				json_response = json.loads(response.content)
				memcache.set(key='service_a_data:json', value=json_response)

			else:
				logging.error('ServiceAHandler() : response.status_code : '+str(response.status_code))
				raise Exception('Bad service response')

			# Return the request
			self.redirect('/')
			return
		except Exception, e:
			logging.error(e)
			self.error(500)



def prepareServiceAHandlerURL():
	xmlString = ''
	
	# Create the XML request string
	xmlString = '<rest-request repositoryUrl="http://localhost:50080" repositoryUsername="roboserver" repositoryPassword="345khrglkjhdfv"><parameters>'		
	xmlString = xmlString + '<variable name="service_a_request">'
	xmlString = xmlString + '<attribute type="Short Text" name="url">http://ec2-46-51-187-180.eu-west-1.compute.amazonaws.com:8180</attribute>'
	xmlString = xmlString + '<attribute type="Short Text" name="session"></attribute>'
	xmlString = xmlString + '<attribute type="Short Text" name="name"></attribute>'
	xmlString = xmlString + '</variable></parameters><output-format-json/></rest-request>'

	return xmlString
	