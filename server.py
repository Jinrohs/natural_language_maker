#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import json
import random
import googlemaps
import urllib2

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

def get_position(_id):
    #response = urllib2.urlopen('http://python.org/')
    #html = response.read()

    #return [35.7084958, -139.8130165]
    return [40.714224, -73.961452]

# intension 意図
# 0: エラー
# 1: 雑談
# 2: 位置情報について
def select_intention(_id=0, data={}):
    cands = []

    cands.append(1)

    if data[POS]:
        cands.append(2)

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

def select_comment(intention=0, data={}):
    if intention == 1:
        comment = generate_zatudan()
    elif intention == 2:
        comment = generate_posinfo(data=data)
    else:
        return "Error!"

    return comment


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
    pos = get_position(_id)
    data[POS] = pos

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

