import requests as req
from flask import Flask
from flask import render_template
from flask import jsonify
import datetime

app = Flask(__name__)

@app.route('/canteen/')
def menu():
    resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen")
    data = resp.json()
    print(data)
    return jsonify(data)


@app.route('/canteen/today')
def today_menu():
    current_date = datetime.datetime.today()
    resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen")
    data = resp.json()
    for d in data:
        if d['day'] == str(current_date.strftime('%e/%m/%Y')).strip():
            print(d)
            return d


@app.route('/canteen/tomorrow')
def tomorrow_menu():
    tomorrow_date = datetime.datetime.today() + datetime.timedelta(days=1)
    resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen")
    data = resp.json()
    for d in data:
        if d['day'] == str(tomorrow_date.strftime('%e/%m/%Y')).strip():
            print(d)
            return d


if __name__ == '__main__':
    app.run()
