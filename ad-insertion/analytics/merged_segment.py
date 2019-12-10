#!/usr/bin/python3

import tempfile
import urllib.request
import urllib.parse
import urllib
import os
import shutil

def delete_merged_segment(segment_path):
    shutil.rmtree(os.path.dirname(segment_path))

def create_merged_segment(init_segment,segment):

    segment_uri = urllib.parse.urlparse(segment)
    init_segment_uri = urllib.parse.urlparse(init_segment)

    if (segment_uri.scheme!="http") or (init_segment_uri.scheme!="http"):
        return None
    
    segment_name = os.path.basename(segment_uri.path)
    init_segment_name = os.path.basename(init_segment_uri.path)
    stream_path = os.path.dirname(init_segment_uri.path)[1:]    
    stream_directory = os.path.join(tempfile.mkdtemp(),
                                    stream_path)
    destination_path = os.path.join(stream_directory,
                                    init_segment_name+".dat")
    os.makedirs(stream_directory,exist_ok=True)
    segment_path = os.path.join(stream_directory,segment_name)
    init_segment_path = os.path.join(stream_directory,init_segment_name)
    
    try:
        urllib.request.urlretrieve(segment,segment_path)
        urllib.request.urlretrieve(init_segment,init_segment_path)
        destination = open(destination_path,'wb')
        shutil.copyfileobj(open(init_segment_path,'rb'),destination)
        shutil.copyfileobj(open(segment_path,'rb'),destination)
        destination.close()
    except requests.exceptions.RequestException as e:  
        print("Request failed " + str(e))
        return None
    
    return destination_path

