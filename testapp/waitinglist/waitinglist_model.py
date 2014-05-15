#!/usr/bin/python

"""
waitinglist_models.py
"""

import logging

from google.appengine.ext import ndb

class WaitingList(ndb.Model):
  """Model for the WaitingList """
  email = ndb.StringProperty(required=True)
  company = ndb.StringProperty(indexed=False)
  founder = ndb.BooleanProperty(default=False)

  count = ndb.IntegerProperty(default=1)


  @staticmethod
  def get_id(email):
    return "<%s>" % str(email).upper()


  @classmethod
  def get_key(self, email):
    model_id = self.get_id(email)
    return ndb.Key(self, str(model_id))


  @classmethod
  def get(self, email=None, company=None, founder=None, fetch_count=999):
    try:
      if email and company and founder:
        return self.query(self.email == email, self.company == company, self.founder == founder).get()
      elif email and company:
        return self.query(self.email == email, self.company == company).get()
      elif company and email==None and founder==None:
        return self.query(self.company == company).fetch(fetch_count)
      elif email:
        return self.get_key(email).get()
      else:
        return self.query().fetch(fetch_count)
    except Exception, e:
      logging.error(e)
      return None


  @classmethod
  def set(self, email, company=None, founder=None):
    try:
      wl = self.get_key(email).get() # KEY.get()
      if wl:
        wl.count += 1
      else:
        wl = self(
            key = self.get_key(email), \
            email = str(email), \
            company = str(company), \
            founder = founder, \
            )
      wl.put()

      return wl

    except Exception, e:
      logging.error(e)
      return None
  
  @classmethod
  def delete(self, email):
    try:
      self.get_key(email).delete()
      logging.info('_testapp - User Key (%s) has been deleted')
    except Exception, e: