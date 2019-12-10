import requests as req
import pickle
from flask import Flask, render_template, request
from flask import jsonify
import datetime
import secretariatDB


app = Flask(__name__)
db = secretariatDB.secretariatDB("scr_DB")

@app.route('/secretariat/add')
def add_secretariat():
    return render_template('add_secretariat.html')


@app.route('/secretariat/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        location = request.form.get('location')
        name = request.form.get('name')
        description = request.form.get('description')
        opening_hours = request.form.get('opening_hours')
        obj = db.addSecretariat(location, name, description, opening_hours)
        return jsonify(obj)


@app.route('/secretariat/<id>')
def get_secretariat(id):
    resp = jsonify(db.showSecretariat(id))
    resp.status_code = 200
    return resp



if __name__ == '__main__':
    app.run()
