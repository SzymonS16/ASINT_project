import requests as req
from flask import Flask, render_template, abort
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
    if data:
        dbLog.addLog(service, 'GET', 'menu list', 200)
    else:
        dbLog.addLog(service, 'GET', 'menu list', 404)
        abort(404, description="Resource not found")
    return jsonify(data)


@app.route('/canteen/today')
def today_menu():
    current_date = datetime.datetime.today()
    resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen")
    data = resp.json()
    if not data:
        dbLog.addLog(service, 'GET', 'menu - today', 404)
        abort(404, description="Resource not found")
    for d in data:
        if d['day'] == str(current_date.strftime('%e/%#m/%Y')).strip():
            dbLog.addLog(service, 'GET', 'menu - today', 200)
            return d
    abort(404, description="Resource not found")


@app.route('/canteen/tomorrow')
def tomorrow_menu():
    tomorrow_date = datetime.datetime.today() + datetime.timedelta(days=1)
    resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen")
    data = resp.json()
    if not data:
        dbLog.addLog(service, 'GET', 'menu - tomorrow', 404)
        abort(404, description="Resource not found")
    for d in data:
        if d['day'] == str(tomorrow_date.strftime('%e/%#m/%Y')).strip():
            dbLog.addLog(service, 'GET', 'menu - tomorrow', 200)
            return d
    abort(404, description="Resource not found")


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003)
