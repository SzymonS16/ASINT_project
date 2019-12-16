import requests as req
from flask import Flask, render_template
from flask import jsonify

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
    events = data['events']

    room_name = data['name']
    floor_id = data['parentSpace']['id']
    uri_b = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + str(floor_id)
    resp_b = req.get(uri_b)
    data_b = resp_b.json()
    building_id = data_b['parentSpace']['id']
    building_name = data_b['parentSpace']['name']
    campus = data_b['topLevelSpace']['name']

    print("CAMPUS:{}, BUILDING:{}, ROOM:{}".format(campus, building_name, room_name))
    return render_template('room.html', dt=events, camp=campus, build=building_name, room=room_name)


###SECRETARIAT###
@app.route('/api/secretariat/<id>')
def get_secretariat(id):
    resp = req.get("http://127.0.0.1:5000/secretariat/" + str(id))
    data = resp.json()
    return render_template('secretariat.html', dt=data)


###CANTEEN###

@app.route('/api/canteen/')
def get_menu():
    resp = req.get("http://127.0.0.1:5000/canteen/")
    data = resp.json()
    print(data)
    return render_template('menu.html', dt=data)

@app.route('/api/canteen/today')
def get_menu_today():
    resp = req.get("http://127.0.0.1:5000/canteen/today")
    data = resp.json()
    day = data['day']
    meal = data['meal']
    return render_template('menu_day.html', day=day, meal=meal)

@app.route('/api/canteen/tomorrow')
def get_menu_tomorrow():
    resp = req.get("http://127.0.0.1:5000/canteen/tomorrow")
    data = resp.json()
    day = data['day']
    meal = data['meal']
    return render_template('menu_day.html', day=day, meal=meal)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)

