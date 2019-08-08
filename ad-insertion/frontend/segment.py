#!/usr/bin/python3

from tornado import web, gen
from zkdata import ZKData
from zkmdata import ZKMData
from schedule import Schedule
from os.path import isfile
import time
import re

zk_prefix="/ad-insertion-frontend"
ad_storage_path="/var/www/adinsert"

class SegmentHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(SegmentHandler, self).__init__(app, request, **kwargs)
        self._sch=Schedule()
        self._usecase={"obj_detection":1, "emotion":0, "face_recognition":0}

    def check_origin(self, origin):
        return True

    def _get_usecase_status(self, name, usecase):
        zk_usecase_path=zk_prefix+"/"+name +"/"+usecase
        zk=ZKMData()
        enable=zk.get(zk_usecase_path)
        zk.close()
        if enable == {}:
            return 0
        return enable

    def _set_usecase_status(self, name, usecase, value):
        zk_usecase_path=zk_prefix+"/"+name +"/"+usecase
        zk=ZKMData()
        zk.set(zk_usecase_path,value)
        zk.close()

    @gen.coroutine
    def get(self):
        stream = self.request.uri.replace("/segment/","")
        stream_base = "/".join(stream.split("/")[:-1])
        print("stream: "+stream, flush=True)
        print("stream_base: "+stream_base, flush=True)
        user = self.request.headers.get('X-USER')
        if not user: 
            self.set_status(400, "X-USER missing in headers")
            return

        # Redirect if this is an AD stream.
        if stream.find("/adstream/") != -1:
            start_time=time.time()
            while time.time()-start_time<=60: # wait if AD is not ready
                print("Testing "+ad_storage_path+"/"+stream, flush=True)
                if isfile(ad_storage_path+"/"+stream):
                    if stream.startswith("hls/"):
                        m1=re.search(".*/(.*)_[0-9]+.ts",stream)
                        if m1:
                            testfile=ad_storage_path+"/"+stream_base+"/"+m1.group(1)+".m3u8.complete"
                            print("Testing "+testfile, flush=True)
                            if isfile(testfile): 
                                self.add_header('X-Accel-Redirect','/adinsert/'+stream)
                                self.set_status(200,'OK')
                                return
                    if stream.startswith("dash/"):
                        m1=re.search(".*/(.*)-(chunk|init).*",stream)
                        if m1:
                            testfile=ad_storage_path+"/"+stream_base+"/"+m1.group(1)+".mpd.complete"
                            print("Testing "+testfile, flush=True)
                            if isfile(testfile): 
                                self.add_header('X-Accel-Redirect','/adinsert/'+stream)
                                self.set_status(200,'OK')
                                return
                yield gen.sleep(0.5)

            self.set_status(404, "AD not ready")
            return

        # Forward the media file request to content provider
        print("Redirecting to /intercept/"+stream, flush=True)
        self.set_header('X-Accel-Redirect','/intercept/' + stream)

        # get zk data for additional scheduling instruction
        zk=ZKData()
        seg_info=zk.get(zk_prefix+"/"+stream_base+"/"+user+"/"+stream.split("/")[-1])
        zk.close()
        if not seg_info: return

        # schedule ad
        if "transcode" in seg_info:
            self._sch.transcode(user, seg_info)
            self._sch.flush()

        # schedule analytics
        if "analytics" in seg_info:
            flag=0
            for usecase in ["obj_detection", "emotion", "face_recognition"]:
                self._usecase[usecase]=self._get_usecase_status(user,usecase)
                flag += self._usecase[usecase]
            if flag == 0:
                self._set_usecase_status(user,"obj_detection",1)
                self._usecase["obj_detection"]=1

            if self._usecase["obj_detection"]==1:
                self._sch.analyze(seg_info, "object_detection")
            if self._usecase["emotion"]==1:
                self._sch.analyze(seg_info, "emotion_recognition")
            if self._usecase["face_recognition"] == 1:
                self._sch.analyze(seg_info, "face_recognition")
            self._sch.flush()

            # delay releasing the stream to combat player caching.
            if "seg_duration" in seg_info and seg_info["seg_time"]:
                yield gen.sleep(max(0,seg_info["seg_duration"]-1.5))

    @gen.coroutine
    def post(self):
        name=str(self.get_argument("name"))
        casename=str(self.get_argument("casename"))
        enable=int(self.get_argument("enable"))
        if casename in ["obj_detection", "emotion", "face_recognition"]:
            self._set_usecase_status(name, casename, enable)
        for usecase in ["obj_detection", "emotion", "face_recognition"]:
            self._usecase[usecase]=self._get_usecase_status(name,usecase)
