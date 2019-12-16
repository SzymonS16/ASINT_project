from flask import Flask, render_template, request, redirect, Response
import requests as req
import logDB


Glogin = None
Gpassword = None

service = 'admin'

app = Flask(__name__)

dbLog = logDB.logDB("log_DB")


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
            uri = "http://127.0.0.1:5000/secretariat/"
            resp = req.get(uri)
            data = resp.json()
            return render_template('adminSecretariat.html', scrs=data)
        else:
            return "Authentication failure"


@app.route('/admin/panel/secretariat/add')
def addSecretariat():
        if Glogin=='admin' and Gpassword=='admin':
            return render_template('add_secretariat.html')
        else:
            return "Authentication failure"


@app.route('/admin/panel/secretariat/edit/<id>')
def editSecretariat(id):
        if Glogin=='admin' and Gpassword=='admin':
            uri = "http://127.0.0.1:5000/secretariat/" + str(id)
            resp = req.get(uri)
            data = resp.json()
            print(data)
            return render_template('adminSecretariatEdit.html', scr=data)
        else:
            return "Authentication failure"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5005)
