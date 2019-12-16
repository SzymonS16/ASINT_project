import requests as req
from flask import Flask, request
from flask import render_template, redirect
from flask import jsonify
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return redirect("static/tt.html")

@app.route('/room', methods=['POST'])
def room():
    if request.method == 'POST':
        data = request.data
        print(str(data))
    return str(data)


@app.route('/secretariat', methods=['POST'])
def secretariat():
    if request.method == 'POST':
        data = request.data
        print(str(data))
    return str(data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003)
    #app.run(host='192.168.3.144', port=8080)
