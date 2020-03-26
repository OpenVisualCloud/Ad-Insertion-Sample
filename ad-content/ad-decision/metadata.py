#!/usr/bin/python3

from tornado import web, gen
import json
import requests
from adkeyword import GetAdKeywords, GetMaxKeyword, GetAttrKeyword
import random
import traceback

ad_decision_post_reponse_template = {
    "source": {
        "uri": "string",
        },
    "keywords": [],
    "overlay": [
        {
        "start_frame": 10,
        "stop_frame": 50,
        "x_ratio" : 0.2,
        "y_ratio" : 0.8,
        "text": "string"
        }
        ]
}

ad_content_server="http://ad-content-service:8080/"

#TODO: add database to store this info
inventory_template = [
    {'uri' : 'http://ad-content-service:8080/car.mp4',
     'navigation_url' : 'http://www.intel.com',
     'keywords' : ['car', 'sports'],
     'duration' : '7'
    },
    {'uri' : 'http://ad-content-service:8080/cat1.mp4',
     'navigation_url' : 'http://www.intel.com',
     'keywords' : ['cat', 'pets'],
     'duration' : '3'
    },
    {'uri' : 'http://ad-content-service:8080/dog4.mp4',
     'navigation_url' : 'http://www.intel.com',
     'keywords' : ['dog', 'pets'],
     'duration' : '7'
    }
]

timeout=30

def clip(adkeyword):
    #num = len(ad_clip["adkeyword"])
    for idx, item in enumerate(ad_clip["adkeyword"]):
        if item != None:
            return item

total_suggestion=0
total_intelligent_suggestion=0

class MetaDataHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(MetaDataHandler, self).__init__(app, request, **kwargs)
        self.inventory = None
        self.keywords = []
        self.user_keywords = []
        
    def check_origin(self, origin):
        return True

    def getclip(self):
        max_matched_idx = -1
        max_matched_num = -1
        for idx_clip, clip in enumerate(self.inventory):
            cur_max_matched_num = -1 
            for idx_item,item in enumerate(self.keywords):
                if item["keyword"] in clip["keywords"]:
                    cur_max_matched_num += item["num"]

            for item in self.user_keywords:
                if item in clip["keywords"]:
                    cur_max_matched_num += 1

            if cur_max_matched_num > max_matched_num:
                max_matched_num = cur_max_matched_num
                max_matched_idx = idx_clip

        global total_suggestion, total_intelligent_suggestion
        total_suggestion=total_suggestion+1
        if max_matched_idx>=0:
            total_intelligent_suggestion=total_intelligent_suggestion+1
        else:
            max_matched_idx = random.randint(0,len(self.inventory)-1)

        print("AD insert Suggestion rate: "+str(total_intelligent_suggestion)+"/"+str(total_suggestion)+ " "+ str(total_intelligent_suggestion*100.0/total_suggestion)+ "%", flush=True)
        return self.inventory[max_matched_idx]["uri"]

    @gen.coroutine
    def get(self):
        self.set_status(200,"OK")
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps([{"MetaDataHandler":"Get"}]))
        self.write(json.dumps([ad_decision_post_reponse_template]))
        self.write(json.dumps(self.inventory))

    @gen.coroutine
    def post(self):
        if self.inventory == None:
            try:
                r = requests.get(ad_content_server+"inventory",timeout=timeout)
                if r.status_code == 200:
                    self.inventory = r.json()
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print("ad content server: Error sending status request " + str(e), flush=True)

        try:
            random.shuffle(self.inventory)
            data = json.loads(self.request.body.decode('utf-8'))
            self.user_name = data["user"]["name"]
            self.user_keywords = data["user"]["keywords"]
            # parse the meta data and choose the keyword, the data is the list of meta data
            self.keywords = GetAdKeywords(data["metadata"])
            # select a ad clip according to the keyword
            response_data = ad_decision_post_reponse_template
            response_data["source"]["uri"] = self.getclip()
            response_data["keywords"] = self.keywords

            self.set_status(200,"OK")
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps([response_data]))
            # debug
            #self.write(json.dumps(self.keywords))
            #self.write(json.dumps(data))

        except:
            print(traceback.format_exc(), flush=True)
            self.set_status(503, "Exception when post")

