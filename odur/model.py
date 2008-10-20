#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal
from google.appengine.ext import db

class DecimalProperty(db.Property):
  data_type = Decimal

  def get_value_for_datastore(self, model_instance):
    value = super(DecimalProperty,
                  self).get_value_for_datastore(model_instance)
    return value

  def make_value_from_datastore(self, value):
    if value is None:
      return None
    return Decimal(value)

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

class PayeeCategory(db.Model):
  name = db.StringProperty(required=True)
  owner = db.UserProperty()

class Payee(db.Model):
  name = db.StringProperty(required=True)
  owner = db.UserProperty()

class Operation(db.Model):
  number = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  p = db.BooleanProperty(default=False)
  description = db.StringProperty()
  payee = db.ReferenceProperty(Payee, required=False)
  categories = db.ReferenceProperty(PayeeCategory, required=False)
  account = db.ReferenceProperty(Account,required=True)
  amount = DecimalProperty(required=True)
