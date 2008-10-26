#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from decimal import Decimal

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from odur.common import addCommonTemplateValues, ref_exists
from odur.generic_viewer import GenericViewer
from odur.model import Account, Bank, Operation, PayeeCategory


class OperationPage(GenericViewer):
  def __init__(self):
    GenericViewer.__init__(self, Operation, '/operation')

  def checkPermissions(self, action):
    if not users.get_current_user():
      self.redirect(users.create_login_url(self.url))
      return False
    return True

  def add(self):
    if GenericViewer.add(self):
      return False
    operation = Operation(
      number = self.request.get('number'),
      date = datetime.strptime(self.request.get('date'),'%m/%d/%Y'),
      description = self.request.get('description'),
      #payee,
      categories = db.get(self.request.get('category')),
      account = db.get(self.request.get('account')),
      amount = self.request.get('amount')
      )
    operation.put()
    self.messages.append('Operation ``%s'' successfully added.'
                         % operation.description)
    self.redirect('/operation?account=' + self.request.get('account'))
    return True

  def delete(self):
    item = db.get(self.request.get('key'))
    if not item or not item.account.owner:
      self.messages.append('Error: invalid operation.')
      self.redirect('/operation?account=' + self.request.get('account'))
      return False
    if (item.account.owner != users.get_current_user()
        and users.is_current_user_admin()):
      self.messages.append(
        'Error: insufficient permissions to delete this account.')
      self.redirect('/operation?account=' + self.request.get('account'))
      return False
    res = GenericViewer.delete(self)
    self.redirect('/operation?account=' + self.request.get('account'))
    return res

  def categoryChart(self, account, showExpense=True, title=None, id=None):
    if account is None:
      return ""
    if not users.is_current_user_admin():
      if account.owner is not users.get_current_user():
        return ""
    if id is None:
      id = "category_chart_" + account.key().__str__()
    if title is None:
      if showExpense:
        title = "Expense by payee category"
      else:
        title = "Takings by payee category"

    operations_query = Operation.all()
    operations_query.filter('account =', account)

    values = {}
    for op in operations_query:
      if showExpense:
        if op.amount < 0:
          if values.has_key(op.categories):
            values[op.categories.name] += -op.amount
          else:
            values[op.categories.name] = -op.amount
      else:
        if op.amount > 0:
          if values.has_key(op.categories):
            values[op.categories.name] += op.amount
          else:
            values[op.categories.name] = op.amount

    str = """
    <script type=\"text/javascript\">
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Category');
        data.addColumn('number', 'Number of operations');
        data.addRows(%i);
"""% (len(values.keys()))

    i = 0
    for k,v in values.iteritems():
      str += "data.setValue(%i, 0,'%s');\n" % (i,k)
      str += "data.setValue(%i, 1,%s);\n" % (i,v)
      i += 1

    str += """
        var chart = new google.visualization.PieChart(document.getElementById('%s'));
        chart.draw(data, {width: 400, height: 240, is3D: true, title: '%s'});
      }
    </script>
    <div id='%s'></div>
""" % (id,title,id)

    return str

  def view(self):
    if not self.request.get('account'):
      self.redirect('/')
      return

    account = db.get (self.request.get('account'))
    if not account or account.owner != users.get_current_user():
      self.redirect('/')
      return

    order = self.request.get('order')
    if order is '':
      order = 'date'

    operations_query = Operation.all()
    operations_query.filter('account =', db.get(self.request.get('account')))
    operations_query.order(order)
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

    categories_query = PayeeCategory.all().order('name')
    categories=[]
    for category in categories_query:
      part = category.name.partition('/')
      if part[1] == '':
        category.root = ''
      else:
        category.root = part[0]
        category.name = part[2]
      categories.append(category)

    template_values = {
      'currency': account.currency,
      'operations': operations,
      'currentAccount': account,
      'amountPositive': currentAmount >= 0,
      'currentCredit': currentCredit,
      'currentDebit': currentDebit,
      'currentAmount': currentAmount,
      'categories': categories,
      'chartExpense': self.categoryChart(account),
      'chartTakings': self.categoryChart(account, showExpense=False)
      }
    addCommonTemplateValues(template_values, self)
    path = os.path.join(os.path.dirname(__file__), 'operation.html')
    self.response.out.write(template.render(path, template_values))
