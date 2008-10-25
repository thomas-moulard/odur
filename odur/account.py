#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from decimal import Decimal

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from odur.common import addCommonTemplateValues
from odur.generic_viewer import GenericViewer
from odur.model import Account, Bank, Operation

class AccountPage(GenericViewer):
  def __init__(self):
    GenericViewer.__init__(self, Account, '/account')

  def checkPermissions(self, action):
    if not users.get_current_user():
      self.redirect(users.create_login_url(self.url))
      return False
    return True

  def getTotalAmount(self,account):
    currentAmount = 0
    operations_query = Operation.all()
    operations_query.filter('account =', account)
    currentAmount=Decimal()
    for op in operations_query:
      currentAmount += Decimal(op.amount)
    return currentAmount

  def add(self):
    if GenericViewer.add(self):
      return False
    account = Account(
      name = self.request.get('account'),
      bank = db.get(self.request.get('bank')),
      owner = users.get_current_user(),
      )
    account.put()
    self.messages.append('Bank successfully added.')
    self.redirect()
    return True

  def delete(self):
    account = db.get(self.request.get('key'))
    if (account.owner != users.get_current_user()
        and users.is_current_user_admin()):
      self.messages.append(
        'Error: insufficient permissions to delete this account.')
      self.redirect()
      return False
    if not GenericViewer.delete(self):
      return False
#TODO: delete bank's operation.
    return True

#TODO: use generic view.
  def view(self):
    if users.get_current_user() == None:
      accounts = None
    else:
      accounts_query = Account.all()
      accounts_query.filter('owner =', users.get_current_user()).order('name')
      accounts = accounts_query.fetch(10)

      for ac in accounts:
        ac.amount = self.getTotalAmount(ac)
        ac.amountPositive = ac.amount > 0

    banks_query = Bank.all().order('name')
    banks = banks_query.fetch(10)


    template_values = {
      'banks': banks,
      }
    addCommonTemplateValues(template_values, self)
    template_values['accounts'] = accounts

    path = os.path.join(os.path.dirname(__file__), 'account.html')
    self.response.out.write(template.render(path, template_values))
