#!/usr/bin/python3

from tornado import web, gen
from tornado.httpclient import AsyncHTTPClient
from os import listdir
import json
from messaging import Producer

kafka_topic="adstats"
archive_root="/var/www/archive"

#TODO: Add database to store statistics
adstats = [
    {'uri' : 'car.mp4',
     'clicked' : 30,
     'watched' : 45
    },
    {'uri' : 'cat1.mp4',
     'clicked' : 15,
     'watched' : 10
    },
    {'uri' : 'dog4.mp4',
     'clicked' : 3,
     'watched' : 1
    },
    {'uri' : 'person.mp4',
     'clicked' : 3,
     'watched' : 1
    }
]

class AdStatsHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(AdStatsHandler, self).__init__(app, request, **kwargs)
        self._cache={}

    def check_origin(self, origin):
        return True

    @gen.coroutine
    def get(self):
        self.set_status(200,"OK")
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(adstats))

        self._producer = Producer()
        self._producer.send(kafka_topic, json.dumps(adstats))
        self._producer.close()

    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))

            for item in adstats:
                if item['uri'] == data['uri']:
                    if data['clicked'] == 1:
                        item['clicked'] += 1
                    if data['watched'] == 1:
                        item['watched'] += 1
            
            self.set_status(200,"OK")

        except Exception as e:
            self.set_status(503, "Ad-content:Exception during post")
