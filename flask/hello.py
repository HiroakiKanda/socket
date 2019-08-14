# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, make_response
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
    
@app.route("/hoge", methods=['GET'])
def getHoge():
    # URLパラメータ
    params = request.args
    response = {}
    if 'param' in params:
        response.setdefault('res', 'param is : ' + params.get('param'))
    return make_response(jsonify(response))

@app.route("/hoge", methods=['POST'])
def postHoge():
    # ボディ(application/json)パラメータ
    params = request.json
    response = {}
    if 'param' in params:
        response.setdefault('res', 'param is : ' + params.get('param'))
    return make_response(jsonify(response))

app.run(host="127.0.0.1", port=5000)