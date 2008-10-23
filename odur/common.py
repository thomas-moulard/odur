#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import users
from google.appengine.ext import db

from odur.model import Account

def addCommonTemplateValues(template_values, handler):
  template_values['currentUser'] = users.get_current_user()
  template_values['loginUrl'] = users.create_login_url('/')
  template_values['logoutUrl'] = users.create_logout_url('/')
  if users.get_current_user() == None:
    accounts = None
  else:
    accounts_query = Account.all()
    accounts_query.filter('owner =', users.get_current_user()).order('name')
    accounts = accounts_query.fetch(10)
  template_values['accounts'] = accounts
  template_values['messages'] = handler.request.get('messages[]',
                                                    allow_multiple=True)


def ref_exists(obj, slot):
  return obj.__dict__['_RESOLVED_' + slot] is not None
