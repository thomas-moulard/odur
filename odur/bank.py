#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required

from odur.common import addCommonTemplateValues
from odur.generic_viewer import GenericViewer
from odur.model import Bank

class BankPage(GenericViewer):
  def __init__(self):
    GenericViewer.__init__(self, Bank, '/bank')

  def checkPermissions(self, action):
    if (action is 'view'
        or action is 'default'):
      return True
    if not users.is_current_user_admin():
      self.messages.append('Insufficient permissions.')
      self.redirect()
      return False
    return True

  @login_required
  def add(self):
    if GenericViewer.add(self):
      return False
    bank = Bank(
      name = self.request.get('name'),
      )
    bank.put()
    self.redirect()
    return True

  @login_required
  def delete(self):
    if not GenericViewer.delete(self):
      return False
#TODO: delete bank's operation.
    return True

  @login_required
  def initializeData(self):
    data=[
      Bank(name='BNP Paribas'),
      Bank(name='Banque de Bretagne'),
      Bank(name=u'Crédit agricole SA'),
      Bank(name='LCL'),
      Bank(name=u'Société générale'),
      Bank(name='Boursorama'),
      Bank(name=u'Crédit du Nord'),
      Bank(name=u'Caisse d\'épargne'),
      Bank(name=u'Groupe Banque populaire'),
      Bank(name=u'BRED'),
      Bank(name=u'Crédit Coopératif'),
      Bank(name=u'CASDEN,'),
      Bank(name=u'Crédit Maritime'),
      Bank(name=u'Natixis'),
      Bank(name=u'Crédit mutuel'),
      Bank(name=u'Crédit industriel et commercial (CIC)'),

      ]
    return GenericViewer.initializeData(self, data)
