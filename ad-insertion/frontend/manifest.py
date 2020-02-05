#!/usr/bin/python3

from tornado import web, gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from zkdata import ZKData
from manifest_hls import parse_hls
from manifest_dash import parse_dash
import requests
import os

zk_manifest_prefix="/ad-insertion-manifest"
content_provider_url = "http://content-provider-service:8080"
ad_storage_root = "/var/www/adinsert"
ad_interval=list(map(int,os.environ["AD_INTERVALS"].split(",")))
ad_duration=int(os.environ.get("AD_DURATION"))
ad_segment=int(os.environ.get("AD_SEGMENT"))
ad_analytic_ahead=int(os.environ.get("AD_ANALYTIC_AHEAD"))
ad_transcode_ahead=int(os.environ.get("AD_TRANSCODE_AHEAD"))

class ManifestHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(ManifestHandler, self).__init__(app, request, **kwargs)
        self.executor=ThreadPoolExecutor()

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _get_manifest(self, stream, user):
        # Retrive the manifest from upstream.
        try:
            r=requests.get(content_provider_url+"/"+stream)
            r.raise_for_status()
            manifest=r.text
        except Exception as e:
            print("Exception: "+str(e), flush=True)
            return str(e)

        # launch zk
        stream_base = "/".join(stream.split("/")[:-1])
        zk_path=zk_manifest_prefix+"/"+stream_base

        # Parse manifest
        minfo={ "segs": {}, "streams": {}, "manifest": "" }
        ad_spec={
            "prefix": "adstream/"+user,
            "path": ad_storage_root+"/"+stream_base,
            "interval": ad_interval, # ad interval (#segments)
            "duration": ad_duration, # ad duration
            "analytic_ahead":ad_analytic_ahead,
            "transcode_ahead":ad_transcode_ahead,
        }

        zk=ZKData()
        if stream.endswith(".m3u8"):
            minfo=parse_hls(
                stream_cp_url=content_provider_url+"/"+stream,
                m3u8=manifest,
                stream_info=zk.get(zk_path+"/"+stream.split("/")[-1]),
                ad_spec=ad_spec,
                ad_segment=ad_segment
            )
        if stream.endswith(".mpd"):
            minfo=parse_dash(
                stream_cp_url=content_provider_url+"/"+stream,
                mpd=manifest,
                ad_spec=ad_spec,
                ad_segment=ad_segment
            )

        # set zk states
        if minfo["streams"]:
            for stream1 in minfo["streams"]:
                zk.set(zk_path+"/"+stream1, minfo["streams"][stream1])
        if minfo["segs"]:
            for seg in minfo["segs"]:
                zk.set(zk_path+"/"+user+"/"+seg, minfo["segs"][seg])

        zk.close()
        return minfo

    @gen.coroutine
    def get(self):
        stream = self.request.uri.replace("/manifest/","")
        print("stream : " + stream, flush = True)
        user = self.request.headers.get('X-USER')
        if not user: 
            self.set_status(400, "X-USER missing in headers")
            return

        minfo=yield self._get_manifest(stream, user)
        if isinstance(minfo, dict):
            self.write(minfo["manifest"])
            self.set_header('content-type',minfo["content-type"])
            self.set_status(200, 'OK')
        else:
            self.set_status(500, str(minfo))
