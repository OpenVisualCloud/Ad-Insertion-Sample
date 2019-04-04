#!/usr/bin/python3

from tornado import web, gen
from tornado.httpclient import AsyncHTTPClient
from os import listdir
import json

account_service_url="http://account-service:8080"
archive_root="/var/www/archive"

class PlayListHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(PlayListHandler, self).__init__(app, request, **kwargs)
        self._cache={}

    def check_origin(self, origin):
        return True

    @gen.coroutine
    def get(self):
        name = str(self.get_argument("name"))

        if name not in self._cache:
            http_client=AsyncHTTPClient()
            r=yield http_client.fetch(account_service_url+"/acct?name="+name)
            self._cache[name]=json.loads(r.body)

        info=self._cache[name]
        if "subscription" not in info:
            self.set_status(404,"USER NOT FOUND")
            return
        print(info)
     
        try:
            streams=[s for s in listdir(archive_root) if s.endswith(".mp4")]
        except:
            self.set_status(404,"VIDEO NOT FOUND")
            return

        if info["subscription"] == "basic":
            streams=streams[0:3]
        print(streams)

        self.set_status(200,"OK")
        self.set_header("Content-Type", "application/json")
        types=[("hls",".m3u8"),("dash",".mpd")]
        self.write(json.dumps([{"name":t[0]+"-"+s,"url":t[0]+"/"+s+"/index"+t[1],"img":"thumbnail/"+s+".png"} for t in types for s in streams]))
