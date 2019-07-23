#!/usr/bin/python3

from tornado import websocket, gen, ioloop
from messaging import Consumer
import json

kafka_topics=["content_provider_sched","seg_analytics_sched","ad_transcode_sched","seg_analytics_data","workloads","adstats","video_analytics_fps"]

class DebugHandler(websocket.WebSocketHandler):
    def __init__(self, app, request, **kwargs):
        super(DebugHandler, self).__init__(app, request, **kwargs)

    def check_origin(self, origin):
        return True

    def open(self):
        self.set_nodelay(True)
        jobs=[]
        
        ioloop.IOLoop.current().spawn_callback(self._read_topics)

    def data_received(self, chunk):
        pass

    @gen.coroutine
    def _read_topics(self):
        jobs=[]
        for topic in kafka_topics:
            jobs.append(self._read_topic(topic))
        yield jobs

    @gen.coroutine
    def _read_topic(self, topic):
        c = Consumer(None)
        while True:
            try:
                for msg in c.debug(topic):
                    if msg:
                        yield self.write_message(json.dumps({"topic":topic,"value":msg}))
                    else:
                        yield gen.sleep(0.05)

            except Exception as e:
                yield self.write_message("Exception:"+str(e))
                print(str(e))

            # sleep and retry
            yield gen.sleep(10)
