#!/usr/bin/python3

from tornado import web
import random

class AcctHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(AcctHandler, self).__init__(app, request, **kwargs)
        self._users={
            "guest": {
                "subscription": "basic",
                "ad-preference": "any",
            },
            "default": {
                "subscription": "universal",
                "ad-preference": "any",
            },
        }
        random.seed()
        for name in ["sophia","emma","isabella","olivia","ava","emily","abigail","mia","madison","elizabeth","sophia","emma","isabella","olivia","ava","emily","abigail","mia","madison","elizabeth"]: 
            self._users[name]={
                "subscription": "universal",
                "ad-preference": ["sports","family"][int(random.random())%2],
            }

    def check_origin(self, origin):
        return True

    def get(self):
        name = str(self.get_argument("name")).lower()
        if name not in self._users: name="default"
        self.set_status(200,"OK")
        self.write(self._users[name])
