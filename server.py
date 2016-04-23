#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import json


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

# intension 意図
# 0: エラー
# 1: 雑談
# 2: 位置情報について


def get_position(_id):
    return [192, 168]

def select_intention(_id=0, pos=""):
    return 1

def select_comment(intension=0):
    return "hoge"

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
    pos = get_position(_id)

    # 意図の決定
    intension = select_intention(_id=_id, pos=pos)

    # コメントの生成
    comment = select_comment(intension=intension)

    # response オブジェクトの生成
    response = {"result":[{"comment":comment}]}

    response = jsonify(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

if __name__ == '__main__':

    _port = 30000
    app.run(host='0.0.0.0', debug=True, port=_port)

