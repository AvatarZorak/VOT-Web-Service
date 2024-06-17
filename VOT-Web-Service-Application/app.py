from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from flask_oidc import OpenIDConnect
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['*'])

app.config['SECRET_KEY'] = 'v519YWstZmoWqRGZGxYFFEYUr9bDLSP2'

app.config['OIDC_CLIENT_SECRETS'] = 'client_secrets.json'
app.config['OIDC_SCOPES'] = ['openid', 'email', 'profile']

oidc = OpenIDConnect(app)


@app.route('/', methods=['POST'])
@oidc.require_login
def hello_world():
    if oidc.user_loggedin:
        return jsonify(oidc.user_getinfo(["email"]))
    else:
        return redirect(url_for('oidc_auth.login'))
    # return "hello world"


@app.route('/callback')
def callback():
    return redirect(url_for('/'))


if __name__ == '__main__':
    app.run("localhost", 5000)
