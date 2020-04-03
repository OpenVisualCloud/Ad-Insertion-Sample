#!/usr/bin/python3

import socket
import datetime
import psutil
import time
import sys
from messaging import Consumer
import json
import ast

kafka_topics=["workload_data"]

info_template = {
    "time": 0,
#    "machine": "xeon",
    "cpu": 0,
    "mem": {},
    "net": {},
    "e2e": {},
    "fps": {},
    "ad": [],
}

playback_info_template={}
analytic_info_template={}
adrate_info_template={"ad_request_tot":0,"ad_request_suc":0}

def mem():
    mem_total = int(psutil.virtual_memory()[0]/1024/1024/1024)
    mem_used = int(psutil.virtual_memory()[3]/1024/1024/1024)
    mem_per = int(psutil.virtual_memory()[2])
    mem_info = {
        'used' : mem_used,
        'per' : mem_per
    }
    return mem_info

def network():
    network_sent = int(psutil.net_io_counters()[0]/8/1024)
    network_recv = int(psutil.net_io_counters()[1]/8/1024)
    network_info = {
        'S' : network_sent,
        'R' : network_recv
    }
    return network_info

def PlaybackTimingMsgHandler(msg,info):
    msgjson = ast.literal_eval(msg)
    user = msgjson["user"]
    stream = msgjson["stream"]
    time = (int)(msgjson["time"])

    if info.get(user,None) == None and stream.find("index.m3u8") > 0:
        info[user]={}
        info[user][time]=time
        info[user][stream]=stream
        info[user]["start"]=time
        info[user]["end"]=time
        info[user]["e2e"]=0
        info[user]["e2e_min"]=1000
        info[user]["e2e_pre"]=0
        info[user]["e2e_tot"]=0
        info[user]["e2e_avg"]=0
        info[user]["e2e_num"]=0
        info[user]["e2e_max"]=0
        return {"min":0,"avg":0,"max":0,user:info[user]["e2e"]}
    elif info.get(user,None) == None:
        return {}

    if time > info[user]["end"]:
        info[user]["end"]=time
    info[user]["e2e"]=info[user]["end"] - info[user]["start"]
    info[user][stream]=stream
    if stream.find("index.m3u8") > 0 and info[user]["e2e"] > 50:
        info[user]["start"]=time
        if info[user]["e2e"] < info[user]["e2e_min"]: info[user]["e2e_min"]=info[user]["e2e"]
        if info[user]["e2e"] > info[user]["e2e_max"]: info[user]["e2e_max"]=info[user]["e2e"]
        info[user]["e2e_pre"]=info[user]["e2e"]
        info[user]["e2e_num"]=info[user]["e2e_num"]+1
        info[user]["e2e_tot"]=info[user]["e2e_tot"]+info[user]["e2e"]
        info[user]["e2e_avg"]=int(info[user]["e2e_tot"]/info[user]["e2e_num"])
        info[user]["start"]=time

    e2e_min=int(min([value["e2e_min"] for key,value in info.items()]))
    e2e_max=int(max([value["e2e_max"] for key,value in info.items()]))
    e2e_tot=0
    e2e_num=0
    e2e_avg=0
    for key,value in info.items():
        e2e_tot=e2e_tot+value["e2e_tot"]
        e2e_num=e2e_num+value["e2e_num"]

    if e2e_num != 0:
        e2e_avg=int(e2e_tot/e2e_num)

    return {"min":e2e_min,"avg":e2e_avg,"max":e2e_max,user:info[user]["e2e"]}

def AnalyticMsgHandler(msg,info):
    msgjson = ast.literal_eval(msg)
    user = msgjson["user"]
    fps = msgjson["fps"]
    machine_fps_avg = msgjson["fps_avg"]
    machine_fps_tot = msgjson["fps_tot"]
    machine_seg_num = msgjson["seg_num"]

    if info.get(user,None) == None:
        info[user]={}
        info[user]["fps"]=fps
        info[user]["fps_avg_machine"]=machine_fps_avg
        info[user]["fps_tot_machine"]=machine_fps_tot
        info[user]["seg_num_machine"]=machine_seg_num
        info[user]["fps_avg"]=int(fps)
        info[user]["fps_tot"]=fps
        info[user]["seg_num"]=1
        info[user]["fps_min"]=fps
        info[user]["fps_max"]=fps
        return {"min":0,"avg":0,"max":0,user:info[user]["fps_avg"]}

    if info[user]["fps"] < info[user]["fps_min"]: info[user]["fps_min"]=info[user]["fps"]
    if info[user]["fps"] > info[user]["fps_max"]: info[user]["fps_max"]=info[user]["fps"]
    info[user]["fps_tot"]=info[user]["fps_tot"]+fps
    info[user]["seg_num"]=info[user]["seg_num"]+1
    info[user]["fps_avg"]=int(info[user]["fps_tot"]/info[user]["seg_num"])

    e2e_min=int(min([value["fps_min"] for key,value in info.items()]))
    e2e_max=int(max([value["fps_max"] for key,value in info.items()]))
    e2e_tot=0
    e2e_num=0
    e2e_avg=0
    for key,value in info.items():
        e2e_tot=e2e_tot+value["fps_tot"]
        e2e_num=e2e_num+value["seg_num"]

    if e2e_num != 0:
        e2e_avg=int(e2e_tot/e2e_num)

    return {"min":e2e_min,"avg":e2e_avg,"max":e2e_max, user:info[user]["fps_avg"]}

def AdRateMsgHandler(msg,info):
    msgjson = ast.literal_eval(msg)
    user = msgjson["user"]
    ad_request_tot = msgjson["ad_request_tot"]
    ad_request_suc = msgjson["ad_request_suc"]
    if ad_request_tot > info["ad_request_tot"]:
        info["ad_request_tot"]=ad_request_tot
        info["ad_request_suc"]=ad_request_suc
    else:
        ad_request_tot=info["ad_request_tot"]
        ad_request_suc=info["ad_request_suc"]
    ad_rate = int(ad_request_suc*100/ad_request_tot)
    return [str(ad_request_suc)+"/"+str(ad_request_tot)+ ","+ str(ad_rate)+ "%"]

if __name__ == "__main__":
    c = Consumer(None)

    if len(sys.argv)>1: prefix=sys.argv[1]
    instance=socket.gethostname()[0:3]
    machine=prefix+instance

    interval=1
    info=info_template
    playback_info=playback_info_template
    analytic_info=analytic_info_template
    adrate_info=adrate_info_template
    while True:
        try:
            print("Workload: listening to messages", flush=True)
            for topic in kafka_topics:
                for msg in c.messages(topic):
                    #print("Workload: "+str(msg)+" "+topic,flush=True)
                    msgjson = ast.literal_eval(msg)
                    msgtype=msgjson["type"]
                    info["time"]=int(time.mktime(datetime.datetime.now().timetuple()))
                    info["cpu"]=psutil.cpu_percent()
                    info["mem"]=mem()
                    info["net"]=network()

                    try:
                       if msgtype == "playback":
                           info["e2e"]=PlaybackTimingMsgHandler(msg,playback_info)
                       if msgtype == "analytic":
                           info["fps"]=AnalyticMsgHandler(msg,analytic_info)
                       if msgtype == "adrate":
                           info["ad"]=AdRateMsgHandler(msg,adrate_info)
                    except Exception as e:
                        print("Workload: "+str(e), flush=True)

                    print(info,flush=True)
        except Exception as e:
            print(str(e))
            time.sleep(interval)
    c.close()
