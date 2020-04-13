import os
from flask import Flask,jsonify, request
import json
import logging
from summarize import summary

app = Flask(__name__)

@app.route('/summary', methods = ['POST'])
def Summary():
    text = request.json['text']
    return jsonify({"key" : summary(text)})
if __name__ == '__main__':
	app.run(host="127.0.0.1", port = 5555, debug=True)