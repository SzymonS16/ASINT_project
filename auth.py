from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
import requests


redirect_uri = "http://127.0.0.1:5000/userAuth" # this is the address of the page on this app

client_id= "1695915081465948" # copy value from the app registration
clientSecret = "PmYUmtFUuIusf5XDPlchqIufydWqlM1tTfobwiW5oKEXodIFUxAp4sgjbAAN8IQgsNQEOC7eEbzkOwyZhh/PWg==" # copy value from the app registration

fenixLoginpage= "https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=%s&redirect_uri=%s"
fenixacesstokenpage = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

loginName = False
userToken = None
userSecret = None
code = False
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("loginPage.html", username=loginName)

@app.route('/private')
def private_page():
    #this page can only be accessed by a authenticated username
    if loginName == False:
        #if the user is not authenticated

        redPage = fenixLoginpage % (client_id, redirect_uri)
        # the app redirecte the user to the FENIX login page
        return redirect(redPage)
    else:
        #if the user ir authenticated
        #we can use the userToken to access the fenix

        params = {'access_token': userToken}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
        if (resp.status_code == 200):
            r_info = resp.json()
            return render_template("privPage.html", username=loginName, name=r_info['name'])
        else:
            return "oops"

@app.route('/userAuth')
def userAuthenticated():
    #This page is accessed when the user is authenticated by the fenix login pagesetup
    #first we get the secret code retuner by the FENIX login
    code = request.args['code']

    # we now retrieve a fenix access token
    payload = {'client_id': client_id, 'client_secret': clientSecret, 'redirect_uri' : redirect_uri, 'code' : code, 'grant_type': 'authorization_code'}
    response = requests.post(fenixacesstokenpage, params = payload)
    if(response.status_code == 200):
        #if we receive the token
        r_token = response.json()
        #if we receive user
        params = {'access_token': r_token['access_token']}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
        r_info = resp.json()

        # we store it
        global loginName
        loginName = r_info['username']
        global userToken
        userToken = r_token['access_token']
        global userSecret
        userSecret = code

        return redirect('/private')
    else:
        return 'oops'


@app.route('/userValidation', methods=['POST'])
def get_user():
    if request.method == 'POST':
        secret = request.form.get('secret')
        print(secret)

    #this page can only be accessed by a authenticated username
    if loginName == False:
        #if the user is not authenticated

        redPage = fenixLoginpage % (client_id, redirect_uri)
        # the app redirecte the user to the FENIX login page
        return redirect(redPage)
    else:
        #if the user is authenticated
        # we can retrieve a fenix access token
        '''
        payload = {'client_id': client_id, 'client_secret': clientSecret, 'redirect_uri': redirect_uri, 'code': secret, 'grant_type': 'authorization_code'}
        response = requests.post(fenixacesstokenpage, params=payload)
        if (response.status_code == 200):
            # if we receive the token
            r_token = response.json()
        '''
        ### receive user data
        #params = {'access_token': r_token['access_token']}
        params = {'access_token': secret}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params=params)
        if (resp.status_code == 200):
            r_info = resp.json()
            print(r_info)
            return render_template("userValidation.html", username=loginName, name=r_info['name'], photo=r_info['photo'])
        else:
            return "oops"


@app.route('/showSecret')
def showSecret():
    #this page can only be accessed by a authenticated username
    if loginName == False:
        #if the user is not authenticated

        redPage = fenixLoginpage % (client_id, redirect_uri)
        # the app redirecte the user to the FENIX login page
        return redirect(redPage)
    else:
        #if the user ir authenticated
        #we can use the userToken to access the fenix

        if userSecret:
            return render_template("secret.html", secret=userToken)
        else:
            return "OPS"



if __name__ == '__main__':
    app.run()
