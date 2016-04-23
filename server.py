#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import json
from flask import Flask, request, jsonify


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


"""Routing: リクエストの URI とメソッドに応じた処理を呼び出し、結果を返す。"""
@app.route('/', methods=['GET'])
def home():
    try:
        satelite_id = request.args['satelite_id']
    except Exception as e:
        print("Oh...")
        exit()
    return satelite_data[satelite_id]["name"]


if __name__ == '__main__':

    _port = 30000
    app.run(host='0.0.0.0', debug=True, port=_port)

