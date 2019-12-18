from flask import Flask, render_template, request, redirect, abort
import requests as req
import logDB


Glogin = None
Gpassword = None

service = 'admin'
app = Flask(__name__)

dbLog = logDB.logDB("log_DB")


@app.route('/admin')
def admin():
    return render_template("loginForm.html")


@app.route('/admin/auth', methods = ['POST', 'GET'])
def userAuthenticated():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if login == 'admin' and password == 'admin':
            global Glogin
            Glogin = login
            global Gpassword
            Gpassword = password
            dbLog.addLog(service, request.method, 'adminPanel', 200)
            return redirect('/admin/panel')
        else:
            dbLog.addLog(service, request.method, 'adminPanel', 401)
            abort(401, description="Unauthorized")
    else:
        dbLog.addLog(service, request.method, 'adminPanel', 400)
        abort(400, description="Bad request")


@app.route('/admin/panel')
def adminPanel():
        if Glogin=='admin' and Gpassword=='admin':
            return render_template('adminPage.html')
        else:
            abort(401, description="Unauthorized")


@app.route('/admin/panel/log')
def adminLog():
        if Glogin=='admin' and Gpassword=='admin':
            logs = dbLog.listAllLogs()
            return render_template('log.html', logs=logs)
        else:
            abort(401, description="Unauthorized")


@app.route('/admin/panel/secretariat')
def adminSecretariat():
        if Glogin=='admin' and Gpassword=='admin':
            uri = "http://127.0.0.1:5002/secretariat"
            resp = req.get(uri)
            if resp.status_code != 200:
                abort(resp.status_code)
            data = resp.json()
            return render_template('adminSecretariat.html', scrs=data)
        else:
            abort(401, description="Unauthorized")


@app.route('/admin/panel/secretariat/add')
def addSecretariat():
        if Glogin=='admin' and Gpassword=='admin':
            return render_template('add_secretariat.html')
        else:
            abort(401, description="Unauthorized")


@app.route('/admin/panel/secretariat/edit/<id>')
def editSecretariat(id):
        if Glogin=='admin' and Gpassword=='admin':
            uri = "http://127.0.0.1:5002/secretariat/" + str(id)
            resp = req.get(uri)
            if resp.status_code != 200:
                abort(resp.status_code)
            data = resp.json()
            print(data)
            return render_template('adminSecretariatEdit.html', scr=data)
        else:
            abort(401, description="Unauthorized")


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
    app.run(host='127.0.0.1', port=5006)
