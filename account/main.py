#!/usr/bin/python3

from tornado import ioloop, web
from tornado.options import define, options, parse_command_line
import acct

app = web.Application([(r'/acct', acct.AcctHandler)])

if __name__ == "__main__":
    define("port", default=8080, help="the binding port", type=int)
    define("ip", default="0.0.0.0", help="the binding ip")
    parse_command_line()
    print("Listening to " + options.ip + ":" + str(options.port))
    app.listen(options.port, address=options.ip)
    ioloop.IOLoop.instance().start()
