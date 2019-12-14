from flask import Flask, render_template, request, redirect, Response
import logDB
import secretariatDB
from flask import jsonify
import json

Glogin = None
Gpassword = None

service = 'admin'

app = Flask(__name__)

dbLog = logDB.logDB("log_DB")
dbSecretariat = secretariatDB.secretariatDB("scr_DB")


@app.route('/admin/')
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
            return "Authentication failure"
    else:
        dbLog.addLog(service, request.method, 'adminPanel', 400)
        return "Bad request"


@app.route('/admin/panel/')
def adminPanel():
        if Glogin=='admin' and Gpassword=='admin':
            return render_template('adminPage.html')
        else:
            return "Authentication failure"


@app.route('/admin/panel/log')
def adminLog():
        if Glogin=='admin' and Gpassword=='admin':
            logs = dbLog.listAllLogs()
            return render_template('log.html', logs=logs)
        else:
            return "Authentication failure"


@app.route('/admin/panel/secretariat')
def adminSecretariat():
        if Glogin=='admin' and Gpassword=='admin':
            scrs = dbSecretariat.listAllSecretariats()
            return render_template('adminSecretariat.html', scrs=scrs)
        else:
            return "Authentication failure"

@app.route('/admin/panel/secretariat/<id>')
def editSecretariat(id):
        if Glogin=='admin' and Gpassword=='admin':
            scr = dbSecretariat.showSecretariat(int(id))
            return render_template('adminSecretariatEdit.html', scr=scr)
        else:
            return "Authentication failure"

@app.route('/admin/panel/secretariat/edit', methods = ['POST'])
def editSecretariatResult():
        if Glogin=='admin' and Gpassword=='admin':
            if request.method == 'POST' and request.form.get('_method') == 'PUT':
                id = int(request.form.get('id'))
                location = request.form.get('location')
                name = request.form.get('name')
                description = request.form.get('description')
                opening_hours = request.form.get('opening_hours')
                if dbSecretariat.editSecretariat(id, location, name, description, opening_hours):
                    dbLog.addLog(service, 'PUT', 'secretariat', 200)
                else:
                    dbLog.addLog(service, 'PUT', 'secretariat', 304)
            return redirect('/admin/panel/secretariat')
        else:
            return "Authentication failure"



if __name__ == '__main__':
    app.run()
