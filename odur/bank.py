#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

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
      self.messages.append('Error: insufficient permissions.')
      self.redirect()
      return False
    return True

  def add(self):
    if GenericViewer.add(self):
      return False
    bank = Bank(
      name = self.request.get('name'),
      country = self.request.get('country'),
      bankCode = self.request.get('bankCode'),
      bicBankCode = self.request.get('bicBankCode'),
      )
    bank.put()
    self.messages.append('Bank successfully added.')
    self.redirect()
    return True

  def delete(self):
    if not GenericViewer.delete(self):
      return False
#TODO: delete bank's operation.
    return True

  def initializeData(self):
    data=[
      Bank(name='BNP Paribas', country='FR', bankCode=30004),
      Bank(name='Banque de Bretagne', country='FR', bankCode=40168),
      Bank(name=u'Crédit agricole SA', country='FR', bankCode=39996),
      Bank(name='LCL', country='FR', bankCode=30048),
      Bank(name=u'Société générale', country='FR', bankCode=30003),
      Bank(name='Boursorama', country='FR', bankCode=21360),
      Bank(name=u'Crédit du Nord', country='FR', bankCode=30076),
      Bank(name=u'Caisse d\'épargne', country='FR', bankCode=14768),
      Bank(name=u'Groupe Banque populaire', country='FR', bankCode=30007),
      Bank(name=u'BRED', country='FR', bankCode=40398),
      Bank(name=u'Crédit Coopératif', country='FR', bankCode=42559),
      Bank(name=u'CASDEN', country='FR'),
      Bank(name=u'Crédit Maritime', country='FR', bankCode=7389),
      Bank(name=u'Natexis', country='FR', bankCode=10061),
      Bank(name=u'Crédit mutuel', country='FR', bankCode=11808),
      Bank(name=u'Crédit industriel et commercial (CIC)', country='FR',
           bankCode=30066),
      ]
    return GenericViewer.initializeData(self, data)
