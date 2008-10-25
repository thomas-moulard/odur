#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from urllib import urlencode

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from odur.common import addCommonTemplateValues

class GenericViewer(webapp.RequestHandler):
    action = None
    model = None
    url = None
    messages = []
    order = None
    limit = 10
    offset = 0

    def __init__(self, model, url):
        self.model = model
        self.url = url


    def checkPermissions(self, action):
        if not users.is_current_user_admin():
            self.messages.append('Error: insufficient permissions.')
            self.redirect()
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
            self.messages.append('Error: no item key given.')
            self.redirect()
            return False
        key = self.request.get('key', allow_multiple=True)
        if not isinstance(key, list):
            key = [key]

        success = True
        for k in key:
            item = db.get(k)
            if item is None:
                self.messages.append('Error: the item ``%s\'\' does not exist.'
                                     % k)
                success = False
            item.delete()

        if success:
            self.messages.append('Item successfully deleted.')
        self.redirect()
        return success

    def initializeData(self, data=None):
        if self.model.all().count() is not 0:
            self.messages.append('Error: database not empty.')
            self.redirect()
            return False
        for i in data:
            i.put()
        self.messages.append('Database successfully initialized.')
        self.redirect()
        return True

    def massModification(self):
        if self.request.get('delete') is not None:
            self.delete()
        return True

    def customizeView(self):
        pass

    def view(self):
        lmodel = self.model.__name__.lower()

        if self.request.get('order'):
            self.order = self.request.get('order')
        if self.request.get('limit'):
            self.limit = int(self.request.get('limit'))
        if self.request.get('offset'):
            self.offset = int(self.request.get('offset'))

        items_query = self.model.all()
        total = items_query.count()
        if self.order is not None:
            items_query.order(self.order)
        items = items_query.fetch(self.limit, self.offset)

        template_values = {
            'limit': self.limit,
            'offset': self.offset,
            'order': self.order,
            'total': total,
            'max_item': min(self.offset + self.limit, total),
            'items': items,
            }
        addCommonTemplateValues(template_values, self)

        if self.offset > 0:
            prev = self.offset - self.limit
            if prev < 0:
                prev = 0
            template_values['prev_url'] = (
                self.url + '?offset=%s' % prev)

        if self.offset + self.limit < total:
            next = self.offset + self.limit
            template_values['next_url'] = (
                self.url + '?offset=%s' % next)

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
        'mass_modification': __callAction(massModification),
        'view': __callAction(view),
        }

    def handleActions(self):
        self.messages = []
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
    def redirect(self, uri = None, permanent=False,
                 extraArgs=None):
        if uri is None:
            uri = self.url
        if not isinstance(extraArgs, dict):
            extraArgs = {}
        extraArgs['messages[]'] =  self.messages
        uri += '?' + urlencode(extraArgs, True)
        return webapp.RequestHandler.redirect(self, uri, permanent)
