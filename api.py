import requests as req
from flask import Flask, render_template
from flask import jsonify
import datetime

app = Flask(__name__)

###ROOMS###

@app.route('/pdw/')
def pdw():
    return "PDW"

@app.route('/api/room/<id>')
def get_room(id):
    uri = "http://127.0.0.1:5000/room/" + str(id)
    resp = req.get(uri)
    data = resp.json()
    dat = jsonify(data)
    print(data[0])
    print("elo")
    #return data[0]
    return render_template('room.html', dt = data)

@app.route('/building/')
def get_building():
    resp = req.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/2448131361101")
    data = resp.json()
    print(data)
    #return jsonify(data)
    return jsonify(data['parentSpace']['name'])

###SECRETARIAT###


###CANTEEN###

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)

