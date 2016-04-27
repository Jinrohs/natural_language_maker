#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from datetime import date
import time
import datetime
from time import mktime
import time
import json
import random
import googlemaps
import urllib2
import requests
import calendar
import datetime

import world_geo

app = Flask(__name__)

satellite_data = {
    "33492": {
        "name": "いぶき",
        "country": "Japan",
        "type": "satellite"
    },
    "29479": {
        "name": "ひので",
        "country": "Japan",
        "type": "satellite"
    },
    "39084": {
        "name": "Landsat 8",
        "country": "USA",
        "type": "satellite"
    },
    "32038": {
        "name": "BREEZE-M DEB",
        "country": "_",
        "type": "deburi"
    },
    "39244": {
        "name": "DEB",
        "country": "_",
        "type": "deburi"
    },
    "36399": {
        "name": "DEB",
        "country": "_",
        "type": "deburi"
    }
}

[POS, TIME, ADDRESS, ID, KNOWLEDGE]=[2, 3, 4, 5, 6]

def get_localtime(unixtime, pos):
    url="https://maps.googleapis.com/maps/api/timezone/json?location=" + str(round(pos[0],7)) + "," + str(round(pos[1], 7)) +"&timestamp=" + unixtime + "&key=AIzaSyC5n6UIB3HT8mifCTzrkU4PSXGcBDL7wYE"
    timeinfo = requests.get(url).json()
    if timeinfo["status"] != "OK":
    	print timeinfo
    	print url
	return None

    loctime = int(unixtime) + timeinfo["rawOffset"] + timeinfo["dstOffset"] 
    now = datetime.datetime.utcfromtimestamp(loctime) # Unix time -> UTC の naive オブジェクト
    return now.hour

## 現在は使えない
#def get_picurl(data={}):
#    zoom = 6
#    (row, col) = find_grid(zoom, data)
#    url="http://map1.vis.earthdata.nasa.gov/wmts-geo/MODIS_Terra_CorrectedReflectance_TrueColor/default/2012-07-09/EPSG4326_250m/6/" + str(row) + "/" + str(col) + ".jpg"
#    return url

def get_position(_id, timestamp):
    url="http://210.140.86.209:5000/lat_lng_alt?time=" + timestamp + "&ids="+_id
    result = requests.get(url).json()
    return [result["ResultSet"][str(_id)]["latitude"], result["ResultSet"][str(_id)]["longitude"]]

# intention 意図
# 0: エラー
# 1: 雑談
# 2: 位置情報について
# 3: 時間情報について
# 4: 住所情報について
# 6: 衛星の豆知識について
# 7: デブリについて
# 8: 生成した雑談
def select_intention(_id=0, data={}):
    cands = []

    print data

    if satellite_data[data[ID]]["type"] == 'deburi':
        return 7

    cands.append(1)

    cands.append(6)
    cands.append(6)
    cands.append(6)

    # ひので
    if data[ID] == '29479':
        cands.append(8)
        cands.append(8)
        cands.append(8)

    if data[POS]:
    	cands.append(2)

    if data[TIME]:
    	cands.append(3)
    	cands.append(3)
    	cands.append(3)
    	cands.append(3)

    if data[ADDRESS]:
    	cands.append(4)
    	cands.append(4)
    	cands.append(4)
    	cands.append(4)
    	cands.append(4)
    	cands.append(4)

    #if not data[TIME] or not data[ADDRESS]:
    #	cands.append(1)
    #else:
    #	if data[POS]:
    #		cands.append(2)
    #
    #	if data[TIME]:
    #		cands.append(3)
    #
    #	if data[ADDRESS]:
    #    	cands.append(4)

    if len(cands) == 0:
	cands.append(1)

    print cands
    res = random.choice(cands)
    return res

def generate_knowledge(data={}):
    if data[ID] == '29479': # ひので
        return random.choice(knowledge_hinode_data)
    elif data[ID] == '33492': # いぶき
        return random.choice(knowledge_ibuki_data)
    elif data[ID] == '39084': # lang8
        return random.choice(knowledge_lang8_data)
    return "宇宙は広いよ"

def generate_zatudan_gene(data={}):
    if data[ID] == '29479': # ひので
        return random.choice(zatudan_hinode_data)
    else:
        return "宇宙は広いよ"

def generate_zatudan(data={}):
    if data[ID] == '29479': # ひので
        return random.choice(zatudan_hinode_data)
    else:
        return random.choice(zatudan_data)

def convert_geocode(lat, lon):
    address = world_geo.convert_geocode(lat, lon)
    #try:
    #    res = gmaps.reverse_geocode((lon, lat))
    #    for r in res[0]["address_components"]:
    #        if 'country' in r['types']:
    #            country = r["long_name"]
    #        if 'administrative_area_level_1' in r['types']:
    #            admin_area = r["long_name"]
    #    address = u"{0}_{1}".format(country, admin_area)
    #except:
    #    address = ""
    print "address:", address
    print "lat, lon:", lat, lon
    return address

def generate_debri(data={}):

    comments = []
    comments.append("...")
    comments.append("ぼくはゴミです...")
    comments.append("...ただ宇宙を漂います")
    return random.choice(comments)

def generate_addressinfo(data={}):

    info = data[ADDRESS]
    comments = []
    comments.append("この辺は{0}かな".format(info))
    comments.append("いま、{0}にいるよ！".format(info))
    return random.choice(comments)

def generate_timeinfo(data={}):
    seed = time.time()
    r1 = random.SystemRandom(seed) 
    comments = []
    if (r1 > 0.9):
    	comments.append("こちらはいま{0}時だよ".format(data[TIME]))
    else:
    	if (data[TIME] >= 23 or data[TIME] < 6):
		comments.append("{0}時だよ. まだ仕事してんの?".format(data[TIME]))
    	if (data[TIME] >= 6 and data[TIME] < 12):
		comments.append("朝だよ")
		comments.append("おはよう")
		comments.append("おはー!")
    	if (data[TIME] >= 12 and data[TIME] < 16):
		comments.append("もうお昼だね")
		comments.append("こんにちはー!")
    	if (data[TIME] >= 16 and data[TIME] < 23):
		comments.append("こんばんはー!")
		comments.append("おやすみなさい")
    return random.choice(comments)

def generate_posinfo(data={}):
    if data[POS][0] > 0:
	lat = "北緯"
    else:
	lat = "南緯"
    if data[POS][1] > 0:
	lon = "東経"
    else:
	lon = "西経"
    info = lat+"{0}度,".format(round(abs(data[POS][0]),1))+lon+"{0}度".format(round(abs(data[POS][1]),1))
    comments = []
    comments.append("{0}に来たよ".format(info))
    comments.append("この辺は{0}かな".format(info))
    comments.append("いま、{0}にいるよ！".format(info))
    return random.choice(comments)

def select_comment(intention=0, data={}):
    if intention == 1:
        comment = generate_zatudan(data=data)
    elif intention == 2:
	comment = generate_posinfo(data=data) 
    elif intention == 3:
	comment = generate_timeinfo(data=data)
    elif intention == 4:
	comment = generate_addressinfo(data=data)
    elif intention == 6:
	comment = generate_knowledge(data=data)
    elif intention == 7:
	comment = generate_debri(data=data)
    elif intention == 8:
	comment = generate_zatudan_gene(data=data)
    else:
        return "Error!"

    return comment

def find_grid(zoom, data={}):
    ngrid = 2 ** zoom
    xmin = -180.0
    xmax = 180.0
    ymin = 85.0
    ymax = -85.0    
    dx = (xmax - xmin)/float(ngrid)
    dy = (ymax - ymin)/float(ngrid)
    nx = int(round((data[POS][0] - xmin)/dx))
    ny = int(round((data[POS][1] - ymin)/dy))	
    return (nx, ny)

@app.route('/', methods=['GET'])
def home():
    try:
        _id       = request.args['id']
        timestamp = request.args['timestamp']
    except Exception as e:
        print("Oh...")
        return "パラメータを正しく設定してください"

    # 状況の取得
    data = {}
    data[ID] = _id
    pos = get_position(_id, timestamp)
    address = convert_geocode(pos[0], pos[1])
    utctime = get_localtime(timestamp, pos)
    data[POS] = pos
    data[ADDRESS] = address
    data[TIME] = utctime

    # 意図の決定
    intention = select_intention(_id=_id, data=data)
    # コメントの生成
    comment = select_comment(intention=intention, data=data)
    print intention, comment
        
    # response オブジェクトの生成
    #response = {"result":[{"message":comment, "id":md5.new(comment).hexdigest()}]}
    msg_id = int(time.mktime(datetime.datetime.now().timetuple())) + int(_id)
    print msg_id
    response = {"result":[{"message":comment, "id":msg_id}]}

    response = jsonify(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

gmaps = googlemaps.Client('AIzaSyC5n6UIB3HT8mifCTzrkU4PSXGcBDL7wYE')
#'AIzaSyBaXrjMRZo2WFyYBAtvamA7ukoW70ttYzY'
with open("zatudan.text") as fp:
    zatudan_data = map(lambda x: x.rstrip(), fp.readlines())
with open("zatudan_hinode.text") as fp:
    zatudan_hinode_data = map(lambda x: x.rstrip(), fp.readlines())
with open("knowledge_hinode.text") as fp:
    knowledge_hinode_data = map(lambda x: x.rstrip(), fp.readlines())
with open("knowledge_ibuki.text") as fp:
    knowledge_ibuki_data = map(lambda x: x.rstrip(), fp.readlines())
with open("knowledge_lang8.text") as fp:
    knowledge_lang8_data = map(lambda x: x.rstrip(), fp.readlines())
with open("worldgeo.csv") as fp:
    world_geo_data = map(lambda x: x.rstrip(), fp.readlines())

if __name__ == '__main__':

    _port = 30000
    app.run(host='0.0.0.0', debug=True, port=_port)


