#!/usr/bin/env python
"""
basehandlers.py
"""

import logging
import os
from datetime import date

import webapp2

from webapp2_extras import sessions
from webapp2_extras import jinja2


class BaseHandler(webapp2.RequestHandler):
	"""
		BaseHandler for all requests

		Holds the auth and session properties so they are reachable for all requests
	"""
	def dispatch(self):
		# Get a session store for this request.
		self.session_store = sessions.get_store(request=self.request)

		try:
			# Dispatch the request.
			webapp2.RequestHandler.dispatch(self)
		finally:
			# Save all sessions.
			self.session_store.save_sessions(self.response)


	def handle_exception(self, exception, debug):
		# Log the error.
		logging.exception(exception)

		page_title = 'Ohh Snap!!'
		page_description = "An Error has Occured"

		# If the exception is a HTTPException, use its error code.
		# Otherwise use a generic 500 error code.
		if isinstance(exception, webapp2.HTTPException):
			if int(exception.code) == 403:
				message = 'Sorry Your request can not be completed!'
			elif int(exception.code) == 404:
				message = 'Oops! I could swear this page was here!'
			else:
				message = 'A server error occurred!'
				
		else:
			page_title = 'Error - 500'
			message = 'A server error occurred!'

		context = {'page_title': page_title, \
					'page_description': page_description, \
					'message': message}

		self.render_response('public/error.html', **context)


	@webapp2.cached_property
	def session(self):
		# Returns a session using the default cookie key.
		return self.session_store.get_session()


	@webapp2.cached_property
	def messages(self):
		return self.session.get_flashes(key='_messages')


	def add_message(self, message, level=None):
		self.session.add_flash(message, level, key='_messages')


	@webapp2.cached_property
	def dev_server(self):
		return os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')


	@webapp2.cached_property
	def jinja2(self):
		# Returns a Jinja2 renderer cached in the app registry.
		j=jinja2.get_jinja2(app=self.app)
		j.environment.globals.update({
			# Set global variables.
			'uri_for': webapp2.uri_for,
			# ...
		})
		def format_datetime(value, format='%H:%M / %d-%m-%Y'):
			return value.strftime(format)

		j.environment.filters['datetime'] = format_datetime
		return j


	def render_response(self, filename, **kwargs):

		if self.messages:
			kwargs['messages'] = self.messages

		self.response.write(self.jinja2.render_template(filename, **kwargs))