import requests as req
from flask import Flask
from flask import jsonify
import datetime

app = Flask(__name__)

@app.route('/alameda/')
def get_buildings():
    resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/2448131360897")
    data = resp.json()
    print(data)
    return jsonify(data)


@app.route('/rooms/<id>')
def get_room(id):
    uri = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + str(id)
    resp = req.get(uri)
    data = resp.json()

    room_name = data['name']
    floor_id = data['parentSpace']['id']
    uri_b = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + str(floor_id)
    resp_b = req.get(uri_b)
    data_b = resp_b.json()
    building_id = data_b['parentSpace']['id']
    building_name = data_b['parentSpace']['name']

    print("ID:{} ROOM:{} B_ID:{} B_NAME:{}".format(id, room_name, building_id, building_name))
    print("-----------------------------------------------------------------------------")
    print(data['events'])
    return jsonify(data['events'])


@app.route('/building/')
def get_building():
    resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/2448131361101")
    data = resp.json()
    print(data)
    #return jsonify(data)
    return jsonify(data['parentSpace']['name'])

if __name__ == '__main__':
    app.run()
