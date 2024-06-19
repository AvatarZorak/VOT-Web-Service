import os

from flask import Flask, redirect, url_for, render_template, request, session, jsonify, g, send_from_directory
import requests
from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, origins=['*'])

app.config['CLIENT_SECRET'] = 'ehAfjucEgNpS3ZujbcVjecxI31wmtBWZ'
app.config['CLIENT_ID'] = 'back-end-client'
app.config['UPLOADS_FOLDER'] = './'
app.config['DB_USER'] = 'maxscale'
app.config['DB_PASSWORD'] = 'mariadb'
app.config['DB_HOST'] = 'localhost'
app.config['DB_PORT'] = 4006
app.config['DB_NAME'] = 'application'


cnx = mysql.connector.connect(
    user=app.config['DB_USER'],
    password=app.config['DB_PASSWORD'],
    host=app.config['DB_HOST'],
    port=app.config['DB_PORT'],
    database=app.config['DB_NAME']
)


def get_user_id(access_token):
    keycloak_response = requests.post(
        url='http://localhost:8080/realms/application/protocol/openid-connect/token/introspect',
        data={'token': f'{access_token}',
              'client_id': f'{app.config["CLIENT_ID"]}',
              'client_secret': f'{app.config["CLIENT_SECRET"]}'
              }
    )

    return keycloak_response.json()['name']


@app.route('/', methods=['POST'])
def hello_world():
    user_id = get_user_id(request.headers.get('Authorization'))

    return user_id, 200


@app.route('/upload', methods=['POST'])
def upload_image():
    user_id = get_user_id(request.headers.get('Authorization'))
    file = request.files['image']

    cursor = cnx.cursor()

    cursor.execute("SELECT count(filename), JSON_ARRAY(filename) FROM images WHERE user_id=%s GROUP BY user_id;", (user_id, ))

    results = cursor.fetchone()
    # count = results[0]
    # filenames = results[1]

    print(results)

    # print(count)
    # print(filenames)

    if results is None:
        count = 0
        filenames = []
    else:
        count = results[0]
        filenames = results[1]

    new_file_format = secure_filename(file.filename).split('.')[-1]
    new_filename = f'{user_id}-{count}.{new_file_format}'

    file.save(os.path.join(app.config['UPLOADS_FOLDER'], new_filename))

    return send_from_directory(app.config['UPLOADS_FOLDER'], new_filename)


if __name__ == '__main__':
    app.run("localhost", 5000)
