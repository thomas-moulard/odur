#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from odur.common import addCommonTemplateValues
from odur.generic_viewer import GenericViewer
from odur.model import PayeeCategory

class PayeeCategoryPage(GenericViewer):
  def __init__(self):
    GenericViewer.__init__(self, PayeeCategory, '/payee-category')

  def checkPermissions(self, action):
    if (action is 'view'
        or action is 'default'):
      return True
    if not users.is_current_user_admin():
      self.messages.append('Error: insufficient permissions.')
      self.redirect()
      return False
    return True

  def add(self):
    if GenericViewer.add(self):
      return False
    payeeCategory = PayeeCategory(
      name = self.request.get('name'),
      )
    if (not users.is_current_user_admin() or
        self.request.get('owner') != ''):
        payeeCategory.owner = users.get_current_user()
    payeeCategory.put()
    self.messages.append('Payee category successfully added.')
    self.redirect()
    return True

  def delete(self):
    payeeCategory = db.get(self.request.get('key'))
    if (not users.is_current_user_admin() and
        payeeCategory.owner != users.get_current_user()):
      self.messsages.append(
        'Error: insufficient permissions to delete this category.')
      return False
    if not GenericViewer.delete(self):
      return False
#TODO: update payee/operation categories.
    return True

  def initializeData(self):
    data=[
      PayeeCategory(name='Expense/Bill\Subscription/Household insurance'),
      PayeeCategory(name='Expense/Bill\Subscription/Service charges'),
      PayeeCategory(name='Expense/Bill\Subscription/Heating'),
      PayeeCategory(name='Expense/Bill\Subscription/Water'),
      PayeeCategory(name='Expense/Bill\Subscription/Electricity'),
      PayeeCategory(name='Expense/Bill\Subscription/Internet'),
      PayeeCategory(name='Expense/Bill\Subscription/Rent'),
      PayeeCategory(name='Expense/Bill\Subscription/Domestic cleaning'),
      PayeeCategory(name='Expense/Bill\Subscription/Cell phone'),
      PayeeCategory(name='Expense/Bill\Subscription/Water'),
      PayeeCategory(name='Expense/Bill\Subscription/Consumer credit'),
      PayeeCategory(name='Expense/Bill\Subscription/Real estate credit'),
      PayeeCategory(name='Expense/Bill\Subscription/Care taking service'),
      PayeeCategory(name='Expense/Bill\Subscription/Domestic employee'),
      PayeeCategory(name='Expense/Bill\Subscription/Phone'),
      PayeeCategory(name='Expense/Bill\Subscription/TV\Cable'),

      PayeeCategory(name='Expense/Food/Coffee house\Bar'),
      PayeeCategory(name='Expense/Food/Grocery'),
      PayeeCategory(name='Expense/Domestic animal/Food'),
      PayeeCategory(name='Expense/Domestic animal/Misc costs'),
      PayeeCategory(name='Expense/Domestic animal/Carer'),
      PayeeCategory(name='Expense/Domestic animal/Veterinary'),

      PayeeCategory(name='Expense/Car\Bike/Accessories'),
      PayeeCategory(name='Expense/Car\Bike/Insurance'),
      PayeeCategory(name='Expense/Car\Bike/Reparation'),
      PayeeCategory(name='Expense/Car\Bike/Gas'),
      PayeeCategory(name='Expense/Car\Bike/Parking\Toll'),
      PayeeCategory(name='Expense/Car\Bike/Credit'),

      PayeeCategory(name='Expense/Misc/Gift'),
      PayeeCategory(name='Expense/Misc/Donation'),
      #Responsabilité civile
      PayeeCategory(name='Expense/Misc/Cash withdrawal'),

      PayeeCategory(name='Expense/Kids/Cultural\Sport activity'),

      PayeeCategory(name='Takings/Salary'),
      ]
    return GenericViewer.initializeData(self, data)
