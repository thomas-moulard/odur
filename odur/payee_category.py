#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from odur.common import addCommonTemplateValues
from odur.model import PayeeCategory

class PayeeCategoryPage(webapp.RequestHandler):
  def add(self):
    if not users.is_current_user_admin():
        if self.request.get('owner') == '':
            return

    payeeCategory = PayeeCategory(
      name = self.request.get('name'),
      )
    if self.request.get('owner') != '':
        payeeCategory.owner = users.get_current_user()
    payeeCategory.put()


#TODO: update payee/operation categories.
  def delete(self):
    if self.request.get('key') == None:
      return
    payeeCategory = db.get(self.request.get('key'))
    if not users.is_current_user_admin():
        if payeeCategory.owner != users.get_current_user():
            return
    payeeCategory.delete()

  def initializeData(self):
    if not users.is_current_user_admin():
      return
    if PayeeCategory.all().count() is not 0:
      return

    PayeeCategory(name='Expense/Culture').put()
    PayeeCategory(name='Expense/Food').put()
    PayeeCategory(name='Expense/Transportation').put()

    PayeeCategory(name='Takings/Salary').put()


  def handleActions(self):
    if self.request.get('action') == 'delete':
      self.delete()
      self.redirect('/payee-category')
    if self.request.get('action') == 'add':
      self.add()
      self.redirect('/payee-category')
    if self.request.get('action') == 'initializeData':
      self.initializeData()
      self.redirect('/payee-category')

  def get(self):
    self.handleActions()
    payeeCategories_query = PayeeCategory.all().order('name')
    payeeCategories = payeeCategories_query.fetch(10)

    template_values = {
      'payeeCategories': payeeCategories,
      }
    addCommonTemplateValues(template_values)
    path = os.path.join(os.path.dirname(__file__), 'payee-category.html')
    self.response.out.write(template.render(path, template_values))


  def post(self):
    self.handleActions()
