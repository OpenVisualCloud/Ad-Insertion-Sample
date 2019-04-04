#!/usr/bin/python3

from tornado import web, gen
from tornado.httpclient import AsyncHTTPClient
from os import listdir
import json

archive_root="/var/www/archive"

class InventoryHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(InventoryHandler, self).__init__(app, request, **kwargs)
        self._cache={}

    def check_origin(self, origin):
        return True

    @gen.coroutine
    def get(self):
        inventory = []
        with open('/home/inventory.json') as f:
            content=f.read()
            inventory = json.loads(str(content))

        self.set_status(200,"OK")
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(inventory))
