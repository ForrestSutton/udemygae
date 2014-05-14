#!/usr/bin/python
'''
waitinglist_model.py
'''

import logging
from google.appengine.ext import ndb

class WaitingList(ndb.Model):
	""" model for waiting list """
   email   = ndb.StringProperty(required=True)
   company = ndb.StringProperty()
   founder = ndb.BooleanProperty(default=False)
   count   = ndb.IntegerProperty(default=1)


   @staticmethod
   def get_id(email):
       return "<%s>" % string(email).upper()
   
   @classmethod 
   def get_key(self, email):
       model_id = self.get_id(email)
       return ndb.Key(self, str(model_id))

   @classmethod
   def set_waitinglist_email(self, form):
   
       email   = form.email.data
       company = form.company.data
       founder = form.founder.data

       try:
           wl = self.get_key(email).get()
           if wl:
               wl.count += 1
               wl.put()
           else:
               wl = self( key = self.get_key(email), \
                                email = str(email), \
                                company = str(company), \
                                founder = founder, \
                                )
               wl.put()

           return wl

       except Exception, e:
           logging.error(e)
           return None
