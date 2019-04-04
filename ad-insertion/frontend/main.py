#!/usr/bin/python3

from tornado import ioloop, web
from tornado.options import define, options, parse_command_line
from manifest import ManifestHandler
from segment import SegmentHandler

app = web.Application([
    (r'/segment/.*',SegmentHandler),
    (r'/manifest/.*',ManifestHandler),
])

if __name__ == "__main__":
    define("port", default=2222, help="the binding port", type=int)
    define("ip", default="127.0.0.1", help="the binding ip")
    parse_command_line()
    print("ad-insertion: frontend: Listening to " + options.ip + ":" + str(options.port), flush = True)
    app.listen(options.port, address=options.ip)
    ioloop.IOLoop.instance().start()
