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

from odur.utils.iso_4217 import ISO_4217

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
      currency = self.request.get('currency'),
      )
    account.put()
    self.messages.append('Account successfully added.')
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
    lmodel = self.model.__name__.lower()

    if self.request.get('order'):
      self.order = self.request.get('order')
    if self.request.get('limit'):
      self.limit = int(self.request.get('limit'))
    if self.request.get('offset'):
      self.offset = int(self.request.get('offset'))

    items_query = self.model.all()
    items_query.filter('owner =', users.get_current_user()).order('name')
    total = items_query.count()
    if self.order is not None:
      items_query.order(self.order)
    items = items_query.fetch(self.limit, self.offset)
    for ac in items:
      ac.amount = self.getTotalAmount(ac)
      ac.amountPositive = ac.amount > 0

    banks = Bank.all().order('name')

    template_values = {
      'banks': banks,
      'limit': self.limit,
      'offset': self.offset,
      'order': self.order,
      'total': total,
      'max_item': min(self.offset + self.limit, total),
      'items': items,
      'iso_4217': ISO_4217,
      }
    addCommonTemplateValues(template_values, self)

    if self.offset > 0:
      prev = self.offset - self.limit
      if prev < 0:
        prev = 0
        template_values['prev_url'] = (
          self.url + '?offset=%s' % prev)

    if self.offset + self.limit < total:
      next = self.offset + self.limit
      template_values['next_url'] = (
        self.url + '?offset=%s' % next)

    path = os.path.join(os.path.dirname(__file__),
                        '%s.html' % lmodel)
    self.response.out.write(template.render(path, template_values))
    return True
