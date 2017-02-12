import os

from flask import Flask, render_template, request, jsonify
from werkzeug.local import LocalProxy
from context import get_db

try:
    from app import config_private as config
except ImportError:
    from app import config_public as config


flask_app = Flask(__name__)
flask_app.config.from_object(config.BaseConfig)
mongo_client = LocalProxy(get_db)

@flask_app.url_defaults
def hashed_static_file_url(endpoint, values):
    """


    :param endpoint:
    :param values:
    :return:

    source:
    https://gist.github.com/Ostrovski/f16779933ceee3a9d181

    """
    if 'static' == endpoint or endpoint.endswith('.static'):
        filename = values.get('filename')
        if filename:
            static_folder = flask_app.static_folder
            blueprint = endpoint.rsplit('.', 1)[0] if '.' in endpoint else request.blueprint
            if blueprint and flask_app.blueprints[blueprint].static_folder:
                static_folder = flask_app.blueprints[blueprint].static_folder
            filepath = os.path.join(static_folder, filename)
            if os.path.exists(filepath):
                values['_'] = int(os.stat(filepath).st_mtime)


def static_file_hash(filename):
    return int(os.stat(filename).st_mtime)


@flask_app.route('/')
def home():
    return render_template('index.html')

@flask_app.route('/signup', methods=['POST'])
def signup():

    email = request.form.get('email')
    password = request.form.get('password')
    
    r = mongo_client.ssw695.users.find_one({"email": email},
                                              {'_id': False})

    if r is not None:
        return 'already signed up!'
    
    user = { 'email' : email,
             'password' : password }

    mongo_client.ssw695.users.insert_one(user)

    return 'successfully signed up!'

@flask_app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    r = mongo_client.ssw695.users.find_one({"email": email},
                                              {'_id': False})

    if r is not None:
        if password != r.get('password'):
            return 'password is not correct.'

        return 'Welcome!'

    return 'User not found.'

@flask_app.route('/about')
def about_page():
    return render_template('about.html')
