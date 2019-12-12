import requests as req
from flask import Flask
from flask import jsonify
import json

app = Flask(__name__)

@app.route('/room/<id>')
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
    campus = data_b['topLevelSpace']['name']

    print("ID:{} ROOM:{} B_ID:{} B_NAME:{} CAMPUS:{}".format(id, room_name, building_id, building_name, campus))
    print("-----------------------------------------------------------------------------")
    print(data['events'][10])
    return jsonify(data)



if __name__ == '__main__':
    app.run()
