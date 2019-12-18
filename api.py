import requests as req
from flask import Flask, render_template, abort

app = Flask(__name__)

###ROOM###
@app.route('/api/room/<id>')
def get_room(id):
    uri = "http://127.0.0.1:5001/room/" + str(id)
    resp = req.get(uri)
    if resp.status_code != 200:
        abort(resp.status_code)
    data = resp.json()
    events = data['events']

    room_name = data['name']
    floor_id = data['parentSpace']['id']
    uri_b = "http://127.0.0.1:5001/floor/" + str(floor_id)
    resp_b = req.get(uri_b)
    if resp_b.status_code != 200:
        abort(resp_b.status_code)
    data_b = resp_b.json()
    building_id = data_b['parentSpace']['id']
    building_name = data_b['parentSpace']['name']
    campus = data_b['topLevelSpace']['name']
    return render_template('room.html', dt=events, camp=campus, build=building_name, room=room_name)


###SECRETARIAT###
@app.route('/api/secretariat/<id>')
def get_secretariat(id):
    resp = req.get("http://127.0.0.1:5002/secretariat/" + str(id))
    if resp.status_code != 200:
        abort(resp.status_code)
    data = resp.json()
    return render_template('secretariat.html', dt=data)


###CANTEEN###
@app.route('/api/canteen/')
def get_menu():
    resp = req.get("http://127.0.0.1:5003/canteen")
    if resp.status_code != 200:
        abort(resp.status_code)
    data = resp.json()
    return render_template('menu.html', dt=data)


@app.route('/api/canteen/today')
def get_menu_today():
    resp = req.get("http://127.0.0.1:5003/canteen/today")
    if resp.status_code != 200:
        abort(resp.status_code)
    data = resp.json()
    day = data['day']
    meal = data['meal']
    return render_template('menu_day.html', day=day, meal=meal)


@app.route('/api/canteen/tomorrow')
def get_menu_tomorrow():
    resp = req.get("http://127.0.0.1:5003/canteen/tomorrow")
    if resp.status_code != 200:
        abort(resp.status_code)
    data = resp.json()
    day = data['day']
    meal = data['meal']
    return render_template('menu_day.html', day=day, meal=meal)


@app.errorhandler(400)
def bad_request_error(error):
    return render_template('400.html'), 400

@app.errorhandler(401)
def auth_error(error):
    return render_template('401.html'), 401

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

