#!/usr/bin/python3

import re
import copy

def _ad_template(ad_spec, name, seq, seg_duration):
    lines=["#EXT-X-DISCONTINUITY"]
    for i in range(int(ad_spec["duration"][seq%len(ad_spec["duration"])]/seg_duration)):
        lines.extend([
            "#EXTINF: " + str(seg_duration) + ",",
            name.format(i),
        ])
    lines.append("#EXT-X-DISCONTINUITY")
    return lines

def _ad_time(ad_spec, seq):
    time=0
    for i in range(seq):
        time=time+ad_spec["duration"][i%len(ad_spec["duration"])]
    return time

def parse_hls(stream_cp_url, m3u8, stream_info, ad_spec, ad_segment=5.0, ad_bench_mode=0):
    lines=m3u8.splitlines()
    if lines[0]!="#EXTM3U": return {}  # invalid m3u8
    if lines[1]!="#EXT-X-VERSION:3": return {}  # format not supported
    stream_cp_url="/".join(stream_cp_url.split("/")[:-1])

    timeline=0.0
    segsplayed=0
    target_duration=3.0
    media_sequence=0
    ad_sequence=0
    minfo={ "segs": {}, "streams": {}, "manifest": [] }
    for i in range(len(lines)):
        if lines[i].startswith("#EXT-X-TARGETDURATION:"):
            m1=re.search("TARGETDURATION:([0-9.]+)",lines[i])
            target_duration=float(m1.group(1))
            timeline=media_sequence*target_duration

        if lines[i].startswith("#EXT-X-MEDIA-SEQUENCE:"):
            m1=re.search("SEQUENCE:([0-9]+)",lines[i])
            media_sequence=int(m1.group(1))
            timeline=media_sequence*target_duration

        if lines[i].startswith("#EXT-X-STREAM-INF:") and i+1<len(lines):
            m1=re.search("BANDWIDTH=([0-9]+)", lines[i])
            m2=re.search("RESOLUTION=([0-9]+)x([0-9]+)", lines[i])
            stream_info={}
            if m1: stream_info["bandwidth"]=int(m1.group(1))
            if m2: stream_info["resolution"]={"width":int(m2.group(1)),"height": int(m2.group(2))}
            if lines[i+1].endswith(".m3u8"):
                minfo["streams"][lines[i+1]]=stream_info

        ad_interval=ad_spec["interval"][ad_sequence%len(ad_spec["interval"])]
        ahead_analytic = ad_interval - 5
        if ahead_analytic < 0: ahead_analytic=0

        if lines[i].startswith("#EXTINF:") and i+1<len(lines):
            m1=re.search("EXTINF:([0-9.]+)", lines[i])
            duration=float(m1.group(1))
            ori_analysis_res=lines[i+1].split("p")[0]
            if int(ori_analysis_res) >= 480:
                dst_analysis_res="480"
            else:
                dst_analysis_res=ori_analysis_res
            seg_info={
                "stream": stream_cp_url.split("/")[-1],
                "resolution": {
                    "width": 0,
                    "height": 0,
                },
                "seg_time": timeline+_ad_time(ad_spec,ad_sequence),
                "seg_duration": duration,
                "codec": "avc",
                "streaming_type": "hls",
                "analytics":[],
                "ad_duration": ad_spec["duration"][ad_sequence%len(ad_spec["duration"])],
                "ad_segment": ad_segment,
            }

            if "resolution" in stream_info.keys():
                seg_info["resolution"]=stream_info["resolution"]

            # schedule every AD_INTERVAL interval
            m1=re.search("(.*)_[0-9]+", lines[i+1])
            ad_name=ad_spec["prefix"]+"/"+str(ad_sequence)+"/"+m1.group(1)
            if segsplayed == ad_interval:
                ad_lines=_ad_template(ad_spec,ad_name+"_{0:03d}.ts",ad_sequence,ad_segment)
                minfo["manifest"].extend(ad_lines)
                ad_sequence=ad_sequence+1
                segsplayed=0

            analytic_info={
                "stream":stream_cp_url+"/"+lines[i+1].replace(ori_analysis_res, dst_analysis_res),
                "seg_time":timeline+_ad_time(ad_spec,ad_sequence)
            }

            if ad_bench_mode != 0:
                line_range=(int)((len(lines)/2+ad_interval-1)/ad_interval)
                if segsplayed == 0 and ad_sequence == 0:
                    for _idy in range(line_range):
                        for _idx in range(_idy*ad_interval+ahead_analytic,(_idy+1)*ad_interval):
                            if i+2*_idx+1<len(lines):
                                temp = analytic_info.copy()
                                temp["stream"]=stream_cp_url+"/"+lines[i+2*_idx+1].replace(ori_analysis_res, dst_analysis_res)
                                temp["seg_time"]=timeline+_ad_time(ad_spec,ad_sequence+_idy)+duration*_idx
                                seg_info["analytics"] +=[temp]
            elif segsplayed == 0 and ad_sequence == 0:
                for _idx in range(ahead_analytic,ad_interval):
                    temp = analytic_info.copy()
                    temp["stream"]=stream_cp_url+"/"+lines[i+2*_idx+1].replace(ori_analysis_res, dst_analysis_res)
                    temp["seg_time"]=timeline+_ad_time(ad_spec,ad_sequence)+duration*_idx
                    seg_info["analytics"] +=[temp]
                for _idx in range(ad_interval+ahead_analytic,2*ad_interval):
                    if i+2*_idx+1<len(lines):
                        temp = analytic_info.copy()
                        temp["stream"]=stream_cp_url+"/"+lines[i+2*_idx+1].replace(ori_analysis_res, dst_analysis_res)
                        temp["seg_time"]=timeline+_ad_time(ad_spec,ad_sequence+1)+duration*_idx
                        seg_info["analytics"] +=[temp]
            elif segsplayed == 0:
                for _idx in range(ad_interval+ahead_analytic,2*ad_interval):
                    if i+2*_idx+1<len(lines):
                        temp = analytic_info.copy()
                        temp["stream"]=stream_cp_url+"/"+lines[i+2*_idx+1].replace(ori_analysis_res, dst_analysis_res)
                        temp["seg_time"]=timeline+_ad_time(ad_spec,ad_sequence+1)+duration*_idx
                        seg_info["analytics"] +=[temp]

            # shedule transcoding every seg
            if ad_bench_mode != 0:
                transcode_info={
                    "stream":ad_spec["path"]+"/"+ad_name+".m3u8",
                    "seg_time":timeline+_ad_time(ad_spec,ad_sequence)+duration*(ad_interval - segsplayed),
                    "bench_mode":ad_bench_mode
                }
                line_range=(int)((len(lines)/2+ad_interval-1)/ad_interval)
                if segsplayed == 0 and ad_sequence == 0:
                    seg_info["transcode"]=[]
                    for k in stream_info: seg_info[k]=stream_info[k]
                    for _idy in range(line_range):
                        _ad_name=ad_spec["prefix"]+"/"+str(_idy)+"/"+m1.group(1)
                        temp = transcode_info.copy()
                        temp["stream"]=ad_spec["path"]+"/"+_ad_name+".m3u8"
                        temp["seg_time"]=timeline+_ad_time(ad_spec,ad_sequence+_idy)+duration*(ad_interval - segsplayed)
                        seg_info["transcode"]+=[temp]
            elif (ad_sequence == 0 and segsplayed == ad_interval - 4) or (ad_sequence != 0 and segsplayed == 1):
                for k in stream_info: seg_info[k]=stream_info[k]
                transcode_info={
                    "stream":ad_spec["path"]+"/"+ad_name+".m3u8",
                    "seg_time":timeline+_ad_time(ad_spec,ad_sequence)+duration*(ad_interval - segsplayed),
                    "bench_mode":ad_bench_mode
                }
                seg_info["transcode"]=[transcode_info]

            # schedule analytics on every segment
            minfo["segs"][lines[i+1]]=seg_info
            timeline=timeline+duration
            segsplayed=segsplayed+1

        minfo["manifest"].append(lines[i])

    minfo["content-type"]="text/plain"
    minfo["manifest"]="\n".join(minfo["manifest"])
    return minfo
