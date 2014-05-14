#!/usr/bin/python
"""
public_handlers.py
"""

import logging
import webapp2
from testapp import basehandler
#from testapp.message import mail_handlers
#import public_forms as forms

#from testapp.waitinglist import waitinglist_models as wl_models

class HomeHandler(basehandler.BaseHandler):
	def get(self):

		page_title = 'testapp - The CrowdFunding Portal'
		page_description = 'testapp - The CrowdFunding Portal'

		context = {'page_title': page_title, \
					'page_description': page_description, \
					#'form_contact': self.form_contact, \
					#'form_waiting': self.form_waiting, \
					#'waiting_action': webapp2.uri_for('waiting_list_submit', _full=True), \
					#'contact_action': webapp2.uri_for('contact_submit', _full=True), \
					}

		self.render_response('public/splash.html', **context)

	@webapp2.cached_property
	def form_contact(self):
		try:
			return forms.ContacttestappForm(self.request.POST)
		except Exception, e:
			logging.error('_testapp Error - HomeHandler(FORM) - %s' % str(e))
			self.abort(403)

	@webapp2.cached_property
	def form_waiting(self):
		try:
			return forms.WaitingListForm(self.request.POST)
		except Exception, e:
			logging.error('_testapp Error - HomeHandler(FORM) - %s' % str(e))
			self.abort(403)


class WaitingListSubmitHandler(basehandler.BaseHandler):
	def post(self):
		if self.form.validate():
			
			email = self.form.email.data
			company = self.form.company.data
			founder = self.form.founder.data

			added = wl_models.WaitingList.set(email, company, founder)
			
			if added:
				complete = mail_handlers.AddedToWaitingListMessage.send_email(email)
				if not complete:
					self.add_message(u"Error sending message to the Email Address - %s" % \
						str(email), 'error')
					logging.error('_testapp Debug - ERROR User NOT added to Waiting List')
			
				self.add_message(u"You (%s) have been added to the Waiting List" % str(email), "success")
				logging.info('_testapp Debug - Email (%s) added to Waiting List' % str(email))
			else:
				self.add_message(u"Error adding the Email Address (%s) to the waiting List." % \
					str(email), 'error')
				logging.error('_testapp Debug - ERROR User NOT added to Waiting List')

		# Form Not Valid
		for field, errors in self.form.errors.items():
			for error in errors:
				self.add_message(u"Error in the %s field - %s" % (
					getattr(self.form, field).label.text,
					error
				), 'error')

		self.redirect(webapp2.uri_for('home', _full=True))

	@webapp2.cached_property
	def form(self):
		try:
			return forms.WaitingListForm(self.request.POST)
		except Exception, e:
			logging.error('_testapp Error - WaitingListSubmitHandler(FORM) - %s' % str(e))
			self.abort(403)


class ContactSubmitHandler(basehandler.BaseHandler):
	def post(self):
		if self.form.validate():
			name = self.form.name.data
			city = self.form.city.data
			email = self.form.email.data
			message = self.form.message.data

			complete = mail_handlers.SendMessageTotestapp.send_email(name, city, email, message)

			if not complete:
				self.add_message(u"Error sending message to testapp", 'error')
		
			self.add_message(u"Thank You, Your message has been sent!", "success")
			logging.info('_testapp - Message has been sent')


		# Form Not Valid
		for field, errors in self.form.errors.items():
			for error in errors:
				self.add_message(u"Error in the ( %s ) form field - %s" % (
					getattr(self.form, field).label.text,
					error
				), 'error')

		self.redirect(webapp2.uri_for('home', _full=True))

	@webapp2.cached_property
	def form(self):
		try:
			return forms.ContacttestappForm(self.request.POST)
		except Exception, e:
			logging.error('_testapp Error - WaitingListSubmitHandler(FORM) - %s' % str(e))
			self.abort(403)