import requests as req
from flask import Flask, render_template, request
from flask import jsonify
import secretariatDB
import logDB
import json

app = Flask(__name__)

db = secretariatDB.secretariatDB("scr_DB")
dbLog = logDB.logDB("log_DB")

service = 'secretariat_service'

@app.route('/secretariat')
def get_secretariat_list():
    secretariats = []
    scrs = db.listAllSecretariats()
    for scr in scrs:
        secretariats.append(scr.__dict__)
    dbLog.addLog(service, 'GET', 'secretariat list', 200)
    return json.dumps(secretariats)


@app.route('/secretariat/<id>')
def get_secretariat(id):
    data = json.dumps(db.showSecretariat(int(id)).__dict__)
    dbLog.addLog(service, 'GET', 'secretariat', 200)
    return data


@app.route('/secretariat/add_result', methods = ['POST'])
def result():
    if request.method == 'POST':
        location = request.form.get('location')
        name = request.form.get('name')
        description = request.form.get('description')
        opening_hours = request.form.get('opening_hours')
        data = json.dumps(db.addSecretariat(location, name, description, opening_hours).__dict__)
        dbLog.addLog(service, 'POST', 'secretariat', 200)
        return data


@app.route('/secretariat/edit_result', methods = ['POST'])
def editSecretariatResult():
    if request.method == 'POST' and request.form.get('_method') == 'PUT':
        id = int(request.form.get('id'))
        location = request.form.get('location')
        name = request.form.get('name')
        description = request.form.get('description')
        opening_hours = request.form.get('opening_hours')
        if db.editSecretariat(id, location, name, description, opening_hours):
            dbLog.addLog(service, 'PUT', 'secretariat', 200)
            return "Resource edited!"
        else:
            dbLog.addLog(service, 'PUT', 'secretariat', 304)
            return "Error! Resource not edited!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
