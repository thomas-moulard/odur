#!/usr/bin/env python

import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from odur.common import addCommonTemplateValues
from odur.account import AccountPage
from odur.bank import BankPage
from odur.operation import OperationPage
from odur.payee_category import PayeeCategoryPage


class MainPage(webapp.RequestHandler):
  def get(self):
    template_values = {}
    addCommonTemplateValues(template_values)
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/', MainPage),
                                        ('/account', AccountPage),
                                        ('/bank', BankPage),
                                        ('/operation', OperationPage),
                                        ('/payee-category', PayeeCategoryPage)
                                        ],
                                       debug=True)
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
