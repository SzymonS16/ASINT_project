import requests as req
from flask import Flask
from flask import jsonify
import datetime
import logDB

app = Flask(__name__)
dbLog = logDB.logDB("log_DB")
service = 'canteen_service'

@app.route('/canteen')
def menu():
    resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen")
    data = resp.json()
    dbLog.addLog(service, 'GET', 'menu list', 200)
    return jsonify(data)


@app.route('/canteen/today')
def today_menu():
    current_date = datetime.datetime.today()
    resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen")
    data = resp.json()
    for d in data:
        if d['day'] == str(current_date.strftime('%e/%m/%Y')).strip():
            dbLog.addLog(service, 'GET', 'menu - today', 200)
            return d


@app.route('/canteen/tomorrow')
def tomorrow_menu():
    tomorrow_date = datetime.datetime.today() + datetime.timedelta(days=1)
    resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen")
    data = resp.json()
    for d in data:
        if d['day'] == str(tomorrow_date.strftime('%e/%m/%Y')).strip():
            dbLog.addLog(service, 'GET', 'menu - tomorrow', 200)
            return d


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003)
