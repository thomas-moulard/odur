#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from decimal import *

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

def addCommonTemplateValues(template_values):
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

class DecimalProperty(db.Property):
  data_type = Decimal

  def get_value_for_datastore(self, model_instance):
    value = super(DecimalProperty,
                  self).get_value_for_datastore(model_instance)
    return value

  def make_value_from_datastore(self, value):
    if value is None:
      return None
    return value

  def validate(self, value):
    v = Decimal(value)
    if value is not None and not isinstance(v, Decimal):
      raise BadValueError('Property %s must be convertible '
                          'to a Decimal instance (%s)' %
                          (self.name, value))
    return super(DecimalProperty, self).validate(value)

  def empty(self, value):
    return not value

class Bank(db.Model):
  name = db.StringProperty(required=True)

class Account(db.Model):
  name = db.StringProperty(required=True)
  bank = db.ReferenceProperty(Bank, required=True)
  dateCreation = db.DateTimeProperty(auto_now_add=True)
  dateUpdate = db.DateTimeProperty(auto_now=True)
  owner = db.UserProperty(required=True)

class Operation(db.Model):
  description = db.StringProperty()
  account = db.ReferenceProperty(required=True)
  amount = DecimalProperty(required=True)

class AccountPage(webapp.RequestHandler):
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

    banks_query = Bank.all().order('name')
    banks = banks_query.fetch(10)


    template_values = {
      'banks': banks,
      }
    addCommonTemplateValues(template_values)
    path = os.path.join(os.path.dirname(__file__), 'account.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    self.handleActions()

class BankPage(webapp.RequestHandler):
  def add(self):
    if not users.is_current_user_admin():
      return
    bank = Bank(
      name = self.request.get('name'),
      )
    bank.put()


  def delete(self):
#TODO: delete bank's operation.
    if not users.is_current_user_admin():
      return
    if self.request.get('key') == None:
      return
    bank = db.get(self.request.get('key'))
    bank.delete()

  def handleActions(self):
    if self.request.get('action') == 'delete':
      self.delete()
      self.redirect('/bank')
    if self.request.get('action') == 'add':
      self.add()
      self.redirect('/bank')

  def get(self):
    self.handleActions()
    banks_query = Bank.all().order('name')
    banks = banks_query.fetch(10)

    template_values = {
      'banks': banks,
      }
    addCommonTemplateValues(template_values)
    path = os.path.join(os.path.dirname(__file__), 'bank.html')
    self.response.out.write(template.render(path, template_values))


  def post(self):
    self.handleActions()

class OperationPage(webapp.RequestHandler):
  def add(self):
    if users.get_current_user() == None:
      return
    operation = Operation(
      description = self.request.get('description'),
      account = db.get(self.request.get('account')),
      amount = self.request.get('amount')
      )
    operation.put()

  def delete(self):
    if users.get_current_user() == None:
      return
    if self.request.get('key') == None:
      return
    operation = db.get(self.request.get('key'))
    if operation.account.owner == users.get_current_user():
      operation.delete()

  def handleActions(self):
    if self.request.get('action') == 'delete':
      self.delete()
      self.redirect('/operation?account=' + self.request.get('account'))
    if self.request.get('action') == 'add':
      self.add()
      self.redirect('/operation?account=' + self.request.get('account'))

  def get(self):
    self.handleActions()

    if not self.request.get('account'):
      self.redirect('/')
      return
    if users.get_current_user() == None:
      self.redirect('/')
      return

    account = db.get (self.request.get('account'))
    if not account or account.owner != users.get_current_user():
      self.redirect('/')
      return

    operations_query = Operation.all()
    operations_query.filter('account =', db.get(self.request.get('account')))
    operations = operations_query.fetch(10)

    currentAmount=Decimal()
    for op in operations:
      currentAmount += Decimal(op.amount)

    template_values = {
      'operations': operations,
      'currentAccount': account,
      'amountPositive': currentAmount >= 0,
      'currentAmount': currentAmount,
      }
    addCommonTemplateValues(template_values)
    path = os.path.join(os.path.dirname(__file__), 'operation.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    self.handleActions()

class MainPage(webapp.RequestHandler):
  def get(self):
    template_values = {}
    addCommonTemplateValues(template_values)
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, template_values))


def main():
  application = webapp.WSGIApplication([('/', MainPage),
                                        ('/account', AccountPage),
                                        ('/bank', BankPage),
                                        ('/operation', OperationPage)],
                                       debug=True)
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
