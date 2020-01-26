#!/usr/bin/python3

from tornado import web, gen
from tornado.httpclient import AsyncHTTPClient
from os import listdir
import json

archive_root="/var/www/archive"

class InventoryHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(InventoryHandler, self).__init__(app, request, **kwargs)
        inventory = []
        with open('/home/inventory.json') as f:
            inventory = json.loads(str(f.read()))
        self._inventory=json.dumps(inventory)

    def check_origin(self, origin):
        return True

    @gen.coroutine
    def get(self):
        self.set_status(200,"OK")
        self.set_header("Content-Type", "application/json")
        self.write(self._inventory)
