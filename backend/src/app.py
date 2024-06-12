from flask import Flask, redirect, url_for, render_template, request, session
from flask_oidc import OpenIDConnect
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = 'v519YWstZmoWqRGZGxYFFEYUr9bDLSP2'

app.config['OIDC_CLIENT_SECRETS'] = 'client_secrets.json'
app.config['OIDC_COOKIE_SECURE'] = False
app.config['OIDC_CALLBACK_ROUTE'] = '/oidc/callback'
app.config['OIDC_SCOPES'] = ['openid', 'email', 'profile']

oidc = OpenIDConnect(app)


@app.route('/')
# @oidc.require_login
def hello_world():
    # if oidc.user_loggedin:
    #     return "Hello world"
    # else:
    #     return redirect(url_for('oidc_auth.login'))
    return "hello world"


if __name__ == '__main__':
    app.run()
