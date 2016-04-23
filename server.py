#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from datetime import date
from time import mktime
import time
import json
import random
import googlemaps
import urllib2
import requests
import calendar
import datetime

app = Flask(__name__)

satelite_data = {
    "33492": {
        "name": "いぶき",
        "id": 33492,
        "country": "Japan"
    },
    "29479": {
        "name": "ひので",
        "id": 29479,
        "country": "Japan"
    },
    "39084": {
        "name": "Landsat 8",
        "id": 39084,
        "country": "USA"
    }
}

[POS]=[0]
[TIME]=[1]

def get_localtime(unixtime, pos):
    url="https://maps.googleapis.com/maps/api/timezone/json?location=" + str(round(pos[0],7)) + "," + str(round(pos[1], 7)) +"&timestamp=" + unixtime
    s = requests.Session() 
    timeinfo = s.get(url).json()
    if timeinfo["status"] == "ZERO_RESULTS":
	return None

    result = int(unixtime) + timeinfo["rawOffset"] + timeinfo["dstOffset"] 
    
    return result

def get_picurl(data={}):
    zoom = 6
    (row, col) = find_grid(zoom, data)
    url="http://map1.vis.earthdata.nasa.gov/wmts-geo/MODIS_Terra_CorrectedReflectance_TrueColor/default/2012-07-09/EPSG4326_250m/6/" + str(row) + "/" + str(col) + ".jpg"
    return url

def get_position(_id, timestamp):
    url="http://210.140.86.209:5000/lat_lng_alt?time=" + timestamp + "&ids="+_id
    s = requests.Session()
    result = s.get(url).json()
    return [result["ResultSet"][str(_id)]["latitude"], result["ResultSet"][str(_id)]["longitude"]]

# intention 意図
# 0: エラー
# 1: 雑談
# 2: 位置情報について
def select_intention(_id=0, data={}):
    cands = []

    cands.append(1)

    if data[POS]:
        cands.append(2)

    if data[TIME]:
    	cands.append(3)
 
    res = random.choice(cands)
    return res

def generate_zatudan():
    return random.choice(zatudan_data)

def convert_geocode(lon, lat):
    try:
        res = gmaps.reverse_geocode((lon, lat))
        for r in res[0]["address_components"]:
            if 'country' in r['types']:
                country = r["long_name"]
            if 'administrative_area_level_1' in r['types']:
                admin_area = r["long_name"]
        address = u"{0}_{1}".format(country, admin_area)
    except:
        address = ""
    return address

def generate_posinfo(data={}):

    address = convert_geocode(data[POS][0], data[POS][1])
    comment = "{0}なう".format(address)

    return comment

def generate_timeinfo(data={}):
    seed = time.time()
    r1 = random.SystemRandom(seed) 
    if (r1 > 0.5):
    	comment = "{0}時なう".format(data[TIME])
    else:
    	if (data[TIME] >= 23 or data[TIME] < 6):
		comment = "{0}時だよ. まだ仕事してんの?" 
    	if (data[TIME] >= 6 and data[TIME] < 12):
		comment = "おはー!"
    	if (data[TIME] >= 12 and data[TIME] < 16):
		comment = "こんにちはー!"
    	if (data[TIME] >= 16 and data[TIME] < 23):
		comment = "こんばんはー!"  
    return comment

def select_comment(intention=0, data={}):
    if intention == 1:
        comment = generate_zatudan()
    elif intention == 2:
        comment = generate_posinfo(data=data)
    elif intention == 3:
	comment = generate_timeinfo(data=data)
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
    pos = get_position(_id, timestamp)
    print 'pos = ', pos
    loctime = get_localtime(timestamp, pos)
    data[POS] = pos
    data[TIME] = None
    if loctime:
    	now = datetime.datetime.utcfromtimestamp(loctime) # Unix time -> UTC の naive オブジェクト
    	data[TIME] = now.hour

    # 意図の決定
    intention = select_intention(_id=_id, data=data)

    # コメントの生成
    comment = select_comment(intention=intention, data=data)
        
    # response オブジェクトの生成
    response = {"result":[{"comment":comment}]}

    response = jsonify(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

gmaps = googlemaps.Client('AIzaSyBaXrjMRZo2WFyYBAtvamA7ukoW70ttYzY')
with open("zatudan.text") as fp:
    zatudan_data = map(lambda x: x.rstrip(), fp.readlines())

if __name__ == '__main__':

    #convert_geocode(35.691219,139.7806127)
    #convert_geocode(42.9882224,141.5292633)
    #exit()

    _port = 30000
    app.run(host='0.0.0.0', debug=True, port=_port)

