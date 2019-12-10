import requests as req
from flask import Flask, render_template, request
from flask import jsonify
import secretariatDB
import json


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
        data = json.dumps(db.addSecretariat(location, name, description, opening_hours).__dict__)
        return data


@app.route('/secretariat/<int:id>')
def get_secretariat(id):
    data = json.dumps(db.showSecretariat(id).__dict__)
    return data


if __name__ == '__main__':
    app.run()
