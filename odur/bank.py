#!/usr/bin/env python

import os

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from odur.common import addCommonTemplateValues
from odur.model import Bank

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
