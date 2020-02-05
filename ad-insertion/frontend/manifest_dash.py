#!/usr/bin/python3

import xml.etree.ElementTree as ET
from copy import deepcopy
import re
import time

#PT0H1M59.89S
def _to_seconds(time):
    s=0
    m=re.search("([0-9.]+)H",time)
    if m: s=s+float(m.group(1))*3600
    m=re.search("([0-9.]+)M",time)
    if m: s=s+float(m.group(1))*60
    m=re.search("([0-9.]+)S",time)
    if m: s=s+float(m.group(1))
    return s

def _to_iso8601(s):
    h=int(s/3600)
    s=s-h*3600
    m=int(s/60)
    s=s-m*60
    return 'PT{0:1g}H{1:1g}M{2:1g}S'.format(h,m,s)

def _to_stream(template, RepresentationID, Number=0):
    template=template.replace("$RepresentationID$","{0}")
    template=re.sub("\$Number\%([0-9]*)d\$",r"{1:\1d}",template)
    return template.format(RepresentationID, Number)

def _ns(tag):
    return "{urn:mpeg:dash:schema:mpd:2011}"+tag;

ET.register_namespace('','urn:mpeg:dash:schema:mpd:2011')
_ad_template=ET.fromstring("""<?xml version="1.0" encoding="utf-8"?>
<MPD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns="urn:mpeg:dash:schema:mpd:2011"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xsi:schemaLocation="urn:mpeg:DASH:schema:MPD:2011 http://standards.iso.org/ittf/PubliclyAvailableStandards/MPEG-DASH_schema_files/DASH-MPD.xsd"
        profiles="urn:mpeg:dash:profile:isoff-live:2011"
        type="static"
        mediaPresentationDuration="PT5S"
        minBufferTime="PT16.6S">
        <ProgramInformation>
        </ProgramInformation>
        <Period id="0" start="PT0.0S">
                <AdaptationSet id="0" contentType="video" segmentAlignment="true" bitstreamSwitching="true" lang="und">
                        <Representation id="0" mimeType="video/mp4" codecs="avc1.640028" bandwidth="2027988" width="1920" height="1080" frameRate="30000/1001">
                                <SegmentTemplate timescale="1000000" duration="5000000" initialization="init-stream0.m4s" media="chunk-stream0-$Number%05d$.m4s" startNumber="1">
                                </SegmentTemplate>
                        </Representation>
                </AdaptationSet>
                <AdaptationSet id="1" contentType="audio" segmentAlignment="true" bitstreamSwitching="true" lang="und">
                        <Representation id="1" mimeType="audio/mp4" codecs="mp4a.40.2" bandwidth="128000" audioSamplingRate="48000">
                                <AudioChannelConfiguration schemeIdUri="urn:mpeg:dash:23003:3:audio_channel_configuration:2011" value="2" />
                                <SegmentTemplate timescale="1000000" duration="5000000" initialization="init-stream1.m4s" media="chunk-stream1-$Number%05d$.m4s" startNumber="1">
                                </SegmentTemplate>
                        </Representation>
                </AdaptationSet>
        </Period>
</MPD>""")

def _ad_time(ad_spec, seq):
    time=0
    for i in range(seq):
        time=time+ad_spec["duration"]
    return time

def _start_number(ad_spec, number, seq):
    for i in range(seq):
        number=number+ad_spec["interval"][i%len(ad_spec["interval"])]
    return number

def _period_index(ad_spec, s):
    i=0
    while True:
        interval=ad_spec["interval"][i%len(ad_spec["interval"])]
        if s<interval: return i
        s=s-interval
        i=i+1

def parse_dash(stream_cp_url, mpd, ad_spec, ad_segment):
    stream_cp_url="/".join(stream_cp_url.split("/")[:-1])

    root=ET.fromstring(mpd)
    mediaPresentationDuration = 0
    if 'mediaPresentationDuration' in root.attrib:
        mediaPresentationDuration=_to_seconds(root.attrib["mediaPresentationDuration"])
    Period=root.find(_ns("Period"))
    formats={
        "video": list(Period.findall(_ns("AdaptationSet[@contentType='video']")+"/"+_ns("Representation"))),
        "audio": list(Period.findall(_ns("AdaptationSet[@contentType='audio']")+"/"+_ns("Representation"))),
    }

    analytic_ahead=ad_spec["analytic_ahead"]
    transcode_ahead=ad_spec["transcode_ahead"]
    # scan all segs into structure
    periods=[]
    for AdaptationSet in Period.findall(_ns("AdaptationSet")):
        sidx=0
        for S in AdaptationSet.findall(_ns("Representation")+"/"+_ns("SegmentTemplate")+"/"+_ns("SegmentTimeline")+"/"+_ns("S")):
            if "t" in S.attrib: t=int(S.attrib["t"])
            d=int(S.attrib["d"])
            r=int(S.attrib["r"]) if "r" in S.attrib else 0

            for repeat in range(r+1):
                pidx=_period_index(ad_spec, sidx)
                if pidx>=len(periods): periods.append({})
                if AdaptationSet not in periods[pidx]: periods[pidx][AdaptationSet]=[]
                periods[pidx][AdaptationSet].append((t,d,sidx))
                sidx=sidx+1
                t=t+d

    # create new periods with ADs
    minfo={"segs":{}, "streams":{} }
    manifest=ET.Element(root.tag, root.attrib)
    for i in range(len(periods)):
        Period1=ET.SubElement(manifest,_ns("Period"),{"id":str(i*2)})

        duration_min=0
        for AdaptationSet in periods[i]:
            AdaptationSet1=ET.SubElement(Period1,_ns("AdaptationSet"),AdaptationSet.attrib)
            Representation1=ET.SubElement(AdaptationSet1,_ns("Representation"),AdaptationSet.find(_ns("Representation")).attrib)

            SegmentTemplate1=ET.SubElement(Representation1,_ns("SegmentTemplate"),AdaptationSet.find(_ns("Representation")+"/"+_ns("SegmentTemplate")).attrib)
            timescale=float(SegmentTemplate1.attrib["timescale"])
            SegmentTemplate1.attrib["presentationTimeOffset"]=str(periods[i][AdaptationSet][0][0])
            SegmentTimeline1=ET.SubElement(SegmentTemplate1,_ns("SegmentTimeline"))

            sidx=0
            duration=0
            ad_interval=ad_spec["interval"][i%len(ad_spec["interval"])]
            ahead_analytic=ad_interval - analytic_ahead
            if ahead_analytic<0: ahead_analytic=0

            for S in periods[i][AdaptationSet]:
                S1=ET.SubElement(SegmentTimeline1,_ns("S"),{"t":str(S[0]),"d":str(S[1])})
                duration=duration+S[1]

                # schedule analytics
                if AdaptationSet.attrib["contentType"]!="video": continue

                # decipher streams
                stream=_to_stream(SegmentTemplate1.attrib["media"],Representation1.attrib["id"],int(SegmentTemplate1.attrib["startNumber"])+S[2])
                init_stream=_to_stream(SegmentTemplate1.attrib["initialization"],Representation1.attrib["id"],int(SegmentTemplate1.attrib["startNumber"])+S[2])

                minfo["segs"][stream]={
                    "stream": stream_cp_url.split("/")[-1],
                    "bandwidth": int(Representation1.attrib["bandwidth"]),
                    "resolution": {
                        "width": int(Representation1.attrib["width"]),
                        "height": int(Representation1.attrib["height"]),
                    },
                    "seg_time": S[0]/timescale+_ad_time(ad_spec,i),
                    "seg_duration": S[1]/timescale,
                    "codec": Representation1.attrib["codecs"],
                    "streaming_type": "dash",
                    "initSeg": stream_cp_url+"/"+init_stream,
                    "analytics": [],
                    "ad_duration": ad_spec["duration"],
                    "ad_segment": ad_segment,
                }

                analytic_info={
                    "stream":stream_cp_url+"/"+stream,
                    "seg_time":S[0]/timescale+_ad_time(ad_spec,i)
                }

                if sidx == 0 and i == 0:
                    for _idx in range(ahead_analytic,ad_interval):
                        temp = analytic_info.copy()
                        stream_to_analytic=_to_stream(SegmentTemplate1.attrib["media"],Representation1.attrib["id"],int(SegmentTemplate1.attrib["startNumber"])+S[2]+_idx)
                        temp["stream"]=stream_cp_url+"/"+stream_to_analytic
                        temp["seg_time"]=S[0]/timescale+_ad_time(ad_spec,i)+(S[1]/timescale)*_idx
                        minfo["segs"][stream]["analytics"] +=[temp]
                    for _idx in range(ad_interval+ahead_analytic,2*ad_interval):
                        temp = analytic_info.copy()
                        stream_to_analytic=_to_stream(SegmentTemplate1.attrib["media"],Representation1.attrib["id"],int(SegmentTemplate1.attrib["startNumber"])+S[2]+_idx)
                        temp["stream"]=stream_cp_url+"/"+stream_to_analytic
                        temp["seg_time"]=S[0]/timescale+_ad_time(ad_spec,i+1)+(S[1]/timescale)*_idx
                        minfo["segs"][stream]["analytics"] +=[temp]
                elif sidx == 0:
                    for _idx in range(ad_interval+ahead_analytic,2*ad_interval):
                        temp = analytic_info.copy()
                        stream_to_analytic=_to_stream(SegmentTemplate1.attrib["media"],Representation1.attrib["id"],int(SegmentTemplate1.attrib["startNumber"])+S[2]+_idx)
                        temp["stream"]=stream_cp_url+"/"+stream_to_analytic
                        temp["seg_time"]=S[0]/timescale+_ad_time(ad_spec,i+1)+(S[1]/timescale)*_idx
                        minfo["segs"][stream]["analytics"] +=[temp]

                if sidx==ad_interval-transcode_ahead:
                    transcode_info={
                        "stream":ad_spec["path"]+"/"+ad_spec["prefix"]+"/"+str(i)+"/"+Representation1.attrib["height"]+"p.mpd",
                        "seg_time":S[0]/timescale+_ad_time(ad_spec,i) + (S[1]/timescale)*(ad_interval -sidx),
                    }
                    minfo["segs"][stream]["transcode"]=[transcode_info]

                #print( minfo["segs"][stream])
                sidx=sidx+1
            SegmentTemplate1.attrib["startNumber"]=str(_start_number(ad_spec, int(SegmentTemplate1.attrib["startNumber"]), i))
            duration=float(duration)/timescale
            if duration<duration_min or duration_min==0: duration_min=duration
        Period1.attrib["duration"]=_to_iso8601(duration_min)
        if(mediaPresentationDuration == 0):
            mediaPresentationDuration += duration_min

        # insert AD
        if i==len(periods)-1: continue   # do not insert AD at the last period
        duration=ad_spec["duration"]
        mediaPresentationDuration += duration
        Period2=ET.SubElement(manifest, _ns("Period"),{"id":str(i*2+1),"duration":_to_iso8601(duration)})
        k=0
        for j in range(len(formats["video"])):
            for AdaptationSet in _ad_template.find(_ns("Period")):
                AdaptationSet1=deepcopy(AdaptationSet)
                contentType=AdaptationSet1.attrib["contentType"]
                if not formats[contentType]: continue

                AdaptationSet1.attrib["id"]=str(k)
                Period2.append(AdaptationSet1)
                k=k+1

                Representation=AdaptationSet1.find(_ns("Representation"))
                for f in ["id","bandwidth","width","height"]:
                    if f in formats[contentType][j].attrib:
                        Representation.attrib[f]=formats[contentType][j].attrib[f]
                SegmentTemplate=Representation.find(_ns("SegmentTemplate"))
                timescale=int(SegmentTemplate.attrib["timescale"])
                SegmentTemplate.attrib["duration"]=str(int(ad_segment*timescale))
                for f in ["initialization","media"]:
                    SegmentTemplate.attrib[f]=ad_spec["prefix"]+"/"+str(i)+"/"+formats["video"][j].attrib["height"]+"p-"+SegmentTemplate.attrib[f]

    manifest.set('mediaPresentationDuration', _to_iso8601(mediaPresentationDuration))
    minfo["manifest"]=ET.tostring(manifest,encoding='utf-8',method='xml')
    minfo["content-type"]="application/xml"
    return minfo
