#!/usr/bin/python3

from tornado import web, gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from zkdata import ZKData
from schedule import Schedule
from os.path import isfile
import traceback
import random
import time
import re
import os

zk_manifest_prefix="/ad-insertion-manifest"
zk_segment_prefix="/ad-insertion-segment"
ad_backoff=str(os.environ["AD_BACKOFF"])
ad_static="/adstatic"

class SegmentHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(SegmentHandler, self).__init__(app, request, **kwargs)
        self._sch=Schedule()
        self.executor=ThreadPoolExecutor()
        self._ads=[x for x in os.listdir("/var/www"+ad_static) if os.path.isdir("/var/www"+ad_static+"/"+x)]
        random.seed()

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _get_segment(self, zk, stream, user, algos):
        stream_base = "/".join(stream.split("/")[:-1])
        segment = stream.split("/")[-1]
        print("stream: "+stream, flush=True)
        print("stream_base: "+stream_base, flush=True)
        print("segment: "+segment, flush=True)

        # Redirect if this is an AD stream
        if stream.find("/adstream/") != -1:
            zk_path=zk_segment_prefix+"/"+stream_base+"/link"
            print("get prefix from "+zk_path, flush=True)
            prefix=zk.get(zk_path)
            print(prefix, flush=True)
            if not prefix:
                zk_path1=zk_segment_prefix+"/"+stream_base+"/backoff"
                prefix=ad_static
                try:
                    backoff=zk.get(zk_path1)
                    if not backoff: backoff=ad_backoff
                    if int(backoff)>0:
                        zk.set(zk_path1,str(int(backoff)-1))
                        return None
                except:
                    print(traceback.format_exc(), flush=True)
            if prefix == ad_static: prefix=prefix+"/"+self._ads[random.randint(0,len(self._ads)-1)]
            return prefix+"/"+segment

        # get zk data for additional scheduling instruction
        seg_info=zk.get(zk_manifest_prefix+"/"+stream_base+"/"+user+"/"+segment)
        if seg_info: 
            # schedule ad
            if "transcode" in seg_info:
                self._sch.transcode(user, seg_info)

            # schedule analytics
            if "analytics" in seg_info:
                if algos.find("object")>=0:
                    self._sch.analyze(user, seg_info, "object_detection")
                if algos.find("emotion")>=0:
                    self._sch.analyze(user, seg_info, "emotion_recognition")
                if algos.find("face")>=0:
                    self._sch.analyze(user, seg_info, "face_recognition")

            if "analytics" in seg_info or "transcode" in seg_info:
                self._sch.flush()

        # redirect to get the media stream
        return '/intercept/' + stream

    @gen.coroutine
    def get(self):
        stream = self.request.uri.replace("/segment/","")
        user = self.request.headers.get('X-USER')
        if not user: 
            self.set_status(400, "X-USER missing in headers")
            return
        algos = self.request.headers.get('X-ALGO')
        print("ALGOS: "+algos, flush=True)
        if not algos: 
            self.set_status(400, "X-ALGO missing in headers")

        zk=ZKData()
        redirect=yield self._get_segment(zk, stream, user, algos)
        zk.close()

        if redirect is None:
            print("Status: 404, AD not ready", flush=True)
            self.set_status(404, "AD not ready")
        else:
            print("X-Accel-Redirect: "+redirect, flush=True)
            if stream.find("/adstream/") != -1: self.add_header('Content-Cache','no-cache')
            self.add_header('X-Accel-Redirect',redirect)
            self.set_status(200,'OK')
