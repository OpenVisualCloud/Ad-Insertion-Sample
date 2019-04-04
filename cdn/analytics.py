#!/usr/bin/python3

from urllib.parse import unquote
from tornado import web
from db import DataBase
import json

class AnalyticsHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(AnalyticsHandler, self).__init__(app, request, **kwargs)
        self._db=DataBase()

    def check_origin(self, origin):
        return True

    def get(self):
        stream=unquote(str(self.get_argument("stream"))).split("/")[-2]
        start=float(self.get_argument("start"))
        end=float(self.get_argument("end"))
        r=self._db.query(stream, [start, end])

        self.set_status(200,'OK')
        self.set_header('Content-Type','application/json')
        self.write(json.dumps(r))
