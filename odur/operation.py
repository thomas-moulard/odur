#!/usr/bin/env python

import os
from datetime import datetime
from decimal import Decimal

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from odur.common import addCommonTemplateValues
from odur.model import Account, Bank, Operation


class OperationPage(webapp.RequestHandler):
  def add(self):
    if users.get_current_user() == None:
      return
    operation = Operation(
      number = self.request.get('number'),
      date = datetime.now(), #FIXME
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
    currentCredit=Decimal()
    currentDebit=Decimal()
    for op in operations:
      amount = Decimal(op.amount)
      if amount < 0:
        op.debit = op.amount
        currentDebit += amount
      else:
        op.credit = op.amount
        currentCredit += amount
      currentAmount += amount

    template_values = {
      'operations': operations,
      'currentAccount': account,
      'amountPositive': currentAmount >= 0,
      'currentCredit': currentCredit,
      'currentDebit': currentDebit,
      'currentAmount': currentAmount,
      }
    addCommonTemplateValues(template_values)
    path = os.path.join(os.path.dirname(__file__), 'operation.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    self.handleActions()
