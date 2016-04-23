#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import json
import random

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
    return [192, 168]

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
    comments = [
    "地球は青いなー",
    "abc"
    ]
    return random.choice(comments)

def generate_posinfo(data={}):
    comment = "{0},{1}なう".format(data[POS][0], data[POS][1])
    return comment

def select_comment(intention=0, data={}):
    if intention == 1:
        comment = generate_zatudan()
    elif intention == 2:
        comment = generate_posinfo(data=data)
    else:
        return "Error!"

    return comment

"""Routing: リクエストの URI とメソッドに応じた処理を呼び出し、結果を返す。"""
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

if __name__ == '__main__':

    _port = 30000
    app.run(host='0.0.0.0', debug=True, port=_port)

