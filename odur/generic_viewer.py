#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from odur.common import addCommonTemplateValues

class GenericViewer(webapp.RequestHandler):
    action = None
    model = None
    url = None

    def __init__(self, model, url):
        self.model = model
        self.url = url

    def checkPermissions(self, action):
        if not users.is_current_user_admin():
            return False
        return True

    # Default actions.
    def add(self):
        return False

    def edit(self):
        return False

    def default(self):
        self.action='view'
        return self.view()

    def delete(self):
        if self.request.get('key') == None:
            return False
        item = db.get(self.request.get('key'))
        if item is None:
            self.redirect(self.url)
            return False
        item.delete()
        self.redirect(self.url)
        return True

    def initializeData(self, data=None):
        if self.model.all().count() is not 0:
            self.redirect()
            return False
        for i in data:
            i.put()
        return True

    def view(self):
        lmodel = self.model.__name__.lower()

        items_query = self.model.all()
        items = items_query.fetch(10)

        template_values = {
            lmodel+'s': items,
            }
        addCommonTemplateValues(template_values)
        path = os.path.join(os.path.dirname(__file__),
                            '%s.html' % lmodel)
        self.response.out.write(template.render(path, template_values))
        return True

    def __callAction(method):
        return lambda self: (self.checkPermissions(method.__name__)
                             and self.__getattribute__(method.__name__)())

    __ACTIONS = {
        'add': __callAction(add),
        'edit': __callAction(edit),
        'delete': __callAction(delete),
        'default': __callAction(default),
        'initializeData': __callAction(initializeData),
        'view': __callAction(view),
        }

    def handleActions(self):
        if self.action is None:
            self.action = self.request.get('action')
        if self.action is '':
            self.action = 'default'
        return self.__ACTIONS[self.action](self)

    def get(self):
        self.handleActions()

    def post(self):
        self.handleActions()


    # Redefine redirec with default URL.
    def redirect(self, uri = None, permanent=False):
        if uri is None:
            return webapp.RequestHandler.redirect(self,
                                                  self.url, permanent)
        else:
            return webapp.RequestHandler.redirect(self,
                                                  uri, permanent)
