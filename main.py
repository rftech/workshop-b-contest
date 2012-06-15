#!/usr/bin/env python
from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.api import memcache
import os
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

# Import local scripts and classes
from controllers import home
from controllers import ods


application = webapp.WSGIApplication([
	('/', home.IndexHandler),
	('/service-a', ods.ServiceAHandler),
	('/task-kickoff/service-a', ods.ServiceAHandler),
	('/tasks/service-a', ods.ServiceAHandler)
	],debug=True)

def main():
	logging.getLogger().setLevel(logging.DEBUG)
	run_wsgi_app(application)

if __name__ == '__main__':
	main()