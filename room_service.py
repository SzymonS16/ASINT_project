import requests as req
from flask import Flask
from flask import jsonify
import json
import logDB

app = Flask(__name__)

dbLog = logDB.logDB("log_DB")

service = 'room_service'
resource = 'room'

@app.route('/room/<id>')
def get_room(id):
    uri = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + str(id)
    resp = req.get(uri)
    data = resp.json()
    dbLog.addLog(service, 'GET', resource, 200)
    return jsonify(data)


@app.route('/floor/<id>')
def get_floor(id):
    floor_id = id
    uri = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + str(floor_id)
    resp = req.get(uri)
    data = resp.json()
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
