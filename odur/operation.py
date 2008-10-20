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
from odur.model import Account, Bank, Operation, PayeeCategory


class OperationPage(webapp.RequestHandler):
  def add(self):
    if users.get_current_user() == None:
      return
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

  def delete(self):
    if users.get_current_user() == None:
      return
    if self.request.get('key') == None:
      return
    operation = db.get(self.request.get('key'))
    if not operation or not operation.account.owner:
      return
    if operation.account.owner == users.get_current_user():
      operation.delete()

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
          values[op.categories] = -op.amount
      else:
        if op.amount > 0:
          values[op.categories] = op.amount

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
      str += "data.setValue(%i, 0,'%s');\n" % (i,k.name)
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


  def handleActions(self):
    if users.get_current_user() == None:
      self.redirect(users.create_login_url('/account'))

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
    addCommonTemplateValues(template_values)
    path = os.path.join(os.path.dirname(__file__), 'operation.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    self.handleActions()
