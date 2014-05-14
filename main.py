#!/usr/bin/env python
"""
main.py
"""

import os

import webapp2
from webapp2_extras import routes

from testapp.public import public_handlers
#from testapp.admin import admin_handlers

DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')


webapp2_config = {}
webapp2_config['webapp2_extras.sessions'] = {
	'secret_key': 'enterasecretkey',
}

app = webapp2.WSGIApplication(
		[
		webapp2.Route(r'/', handler=public_handlers.HomeHandler, name='home'),
		webapp2.Route(r'/contact_submit', handler=public_handlers.ContactSubmitHandler, name='contact_submit'),
		#webapp2.Route(r'/waiting_list_submit', handler=public_handlers.WaitingListSubmitHandler, name='waiting_list_submit'),
		#webapp2.Route(r'/admin', handler=admin_handlers.AdminPageHandler, name='admin_page'),
		#webapp2.Route(r'/add_waitinglist', handler=admin_handlers.AddWaitinglistHandler, name='admin_add_waitinglist'),
		#webapp2.Route(r'/delete_waitinglist', handler=admin_handlers.DeleteWaitinglistHandler, name='admin_delete_waitinglist'),
		
		],
        config=webapp2_config, debug=DEBUG)
