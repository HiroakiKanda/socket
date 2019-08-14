# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    str_out = "<h1 style='color:blue'>Hello There!</h1>"
    str_out += "こんにちは。<p />"
    str_out += "Jul/11/2017<br />"
    str_out += "AM 08:54<br />"
    return str_out

if __name__ == "__main__":
    app.run(host='0.0.0.0')