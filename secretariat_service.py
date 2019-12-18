from flask import Flask, render_template, request, abort
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
    scr = db.showSecretariat(int(id))
    if scr:
        data = json.dumps(scr.__dict__)
    else:
        dbLog.addLog(service, 'GET', 'secretariat', 404)
        abort(404, description="Resource not found")
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
            return "Resource not edited!"


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
