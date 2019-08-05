#!/usr/bin/python3

from tornado import web
from tornado.httpclient import AsyncHTTPClient
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from zkdata import ZKData
from zkmdata import ZKMData
from manifest_hls import parse_hls
from manifest_dash import parse_dash
import os

zk_prefix="/ad-insertion-frontend"
content_provider_url = "http://content-provider:8080"
ad_storage_root = "/var/www/adinsert"

class ManifestHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(ManifestHandler, self).__init__(app, request, **kwargs)
        self.executor=ThreadPoolExecutor()
        self.benchmode=0

    def check_origin(self, origin):
        return True

    def _get_bench_mode(self, name):
        zk_benchmode_path=zk_prefix+"/"+name +"/"+"benchmode"
        zk=ZKMData()
        enable=zk.get(zk_benchmode_path)
        zk.close()
        if enable == {}:
            return 0
        return enable

    @run_on_executor
    def _set_states(self, minfo, zk_path, stream_base, user):
        zk=ZKData()
        if minfo["streams"]:
            for stream1 in minfo["streams"]:
                zk.set(zk_path+"/"+stream1, minfo["streams"][stream1])
        if minfo["segs"]:
            for seg in minfo["segs"]:
                zk.set(zk_path+"/"+user+"/"+seg, minfo["segs"][seg])
        zk.close()

    # fetching manifest 
    async def _fetch_manifest(self, url):
        client=AsyncHTTPClient()
        req = await client.fetch(url)
        return req.body.decode('utf-8')

    async def get(self):
        stream = self.request.uri.replace("/manifest/","")
        print("stream : " + stream, flush = True)
        user = self.request.headers.get('X-USER')
        if not user: 
            self.set_status(400, "X-USER missing in headers")
            return

        # Redirect if this is an AD stream.
        #if stream.find("/adstream/") != -1:
        #    self.set_header('X-Accel-Redirect','/adinsert/' + stream)
        #    self.set_status(200,'OK')
        #    return

        # Retrive the manifest from upstream.
        try:
            manifest=await self._fetch_manifest(content_provider_url+"/"+stream)
        except Exception as e:
            print(str(e))
            self.set_status(500, str(e))
            return

        # launch zk
        stream_base = "/".join(stream.split("/")[:-1])
        zk_path=zk_prefix+"/"+stream_base

        # Parse manifest
        minfo={ "segs": {}, "streams": {}, "manifest": "" }
        ad_spec={
            "prefix": "adstream/"+user,
            "path": ad_storage_root+"/"+stream_base,
            "interval": list(map(int,os.environ.get("AD_INTERVALS").split(","))),    # ad interval (#segments)
            "duration": list(map(int,os.environ.get("AD_DURATION").split(","))),    # ad duration
        }

        ad_bench_mode=self._get_bench_mode(user)
        print("Bench Mode:"+str(ad_bench_mode),flush=True)
        if stream.endswith(".m3u8"):
            zk=ZKData()
            minfo=parse_hls(
                stream_cp_url=content_provider_url+"/"+stream,
                m3u8=manifest,
                stream_info=zk.get(zk_path+"/"+stream.split("/")[-1]),
                ad_spec=ad_spec,
                ad_bench_mode=ad_bench_mode
            )
            zk.close()
        if stream.endswith(".mpd"):
            minfo=parse_dash(
                stream_cp_url=content_provider_url+"/"+stream,
                mpd=manifest,
                ad_spec=ad_spec,
                ad_bench_mode=ad_bench_mode
            )

        # set zk states
        self.executor.submit(self._set_states,minfo,zk_path,stream_base,user)

        # return the manifest
        self.write(minfo["manifest"])
        self.set_header('content-type',minfo["content-type"])
        #print("Manifest: "+minfo["manifest"], flush=True)

    def post(self):
        name=str(self.get_argument("name"))
        enable=int(self.get_argument("enable"))
        zk_benchmode_path=zk_prefix+"/"+name +"/"+"benchmode"
        zk=ZKMData()
        zk.set(zk_benchmode_path, enable)
        zk.close()
