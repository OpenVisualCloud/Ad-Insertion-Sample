#!/usr/bin/python3

from tornado import web, gen
from os.path import isfile
from messaging import Producer
import time

kafka_topic="content_provider_sched"
dashls_root="/var/www/video"

class ScheduleHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(ScheduleHandler, self).__init__(app, request, **kwargs)

    def check_origin(self, origin):
        return True

    @gen.coroutine
    def get(self):
        stream=self.request.uri.replace("/schedule/","")

        # schedule producing the stream
        print("request received to process stream: "+stream, flush=True)
        producer=Producer()
        producer.send(kafka_topic,stream)
        producer.close()

        # wait until file is available, return it
        start_time=time.time()
        while time.time()-start_time<60:
            if isfile(dashls_root+"/"+stream):
                self.set_header('X-Accel-Redirect','/'+stream)
                self.set_status(200, "OK")
                return
            yield gen.sleep(0.5)

        # wait too long, skip this REST API
        self.set_status(503, "Request scheduled")
