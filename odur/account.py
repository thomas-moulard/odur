#!/usr/bin/env python

import os
from decimal import Decimal

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from odur.common import addCommonTemplateValues
from odur.model import Account, Bank, Operation

class AccountPage(webapp.RequestHandler):
  def getTotalAmount(self,account):
    currentAmount = 0
    operations_query = Operation.all()
    operations_query.filter('account =', account)
    currentAmount=Decimal()
    for op in operations_query:
      currentAmount += Decimal(op.amount)
    return currentAmount

  def add(self):
    if users.get_current_user() == None:
      return
    account = Account(
      name = self.request.get('account'),
      bank = db.get(self.request.get('bank')),
      owner = users.get_current_user(),
      )
    account.put()

  def delete(self):
    if users.get_current_user() == None:
      return
    if self.request.get('key') == None:
      return
    account = db.get(self.request.get('key'))
    if account.owner == users.get_current_user():
      account.delete()

  def handleActions(self):
    if self.request.get('action') == 'delete':
      self.delete()
      self.redirect('/account')
    if self.request.get('action') == 'add':
      self.add()
      self.redirect('/account')

  def get(self):
    self.handleActions()

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
    addCommonTemplateValues(template_values)
    template_values['accounts'] = accounts

    path = os.path.join(os.path.dirname(__file__), 'account.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    self.handleActions()
