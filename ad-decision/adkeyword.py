#!/usr/bin/python3

keyword_template=[
    {
        "keyword" : "john",
        "num" : 3,
        "attr" : "face_id"
    },
    {
        "keyword" : "angry",
        "num" : 3,
        "attr" : "emotion"
    },
    {
        "keyword" : "car",
        "num" : 3,
        "attr" : "object"
    }
]

def PutKeyword(keywords, label, attr):
    found = None
    for idx,item in enumerate(keywords):
        if item["keyword"] == label:
            item["num"] += 1
            keywords[idx]["num"] = item["num"]
            found = 1
            break
    if found == None:
       keywords += [{"keyword":label,"num" : 1,"attr":attr}]

def GetMaxKeyword(keywords):
    keyword = None
    max = 0
    for idx,item in enumerate(keywords):
        if item["num"] > max:
            keyword = item["keyword"]
            max = item["num"]
    return keyword

def GetAttrKeyword(keywords, attr):
    keyword = None
    for idx,item in enumerate(keywords):
        if item["attr"] == attr:
            keyword = item["keyword"]
            break
    return keyword

def GetAdKeywords(data):
    try:
        keywords = []
        for frame in data:
            for item in frame["objects"]:
                attr = item["detection"]["label"]
                if attr == "face":
                    sub_item = item.get("emotion")
                    if sub_item != None:
                        PutKeyword(keywords, sub_item["label"], "emotion")
                    sub_item = item.get("face_id")
                    if sub_item != None:
                        PutKeyword(keywords, sub_item["label"], "face_id")
                else:
                    label = item["detection"]["label"]
                    if label != None:
                        PutKeyword(keywords, label, "object")
        return keywords
    except Exception as e:
        print(str(e))

