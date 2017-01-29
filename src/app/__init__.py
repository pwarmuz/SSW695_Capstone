import os

from flask import Flask, render_template, jsonify, abort, request
from werkzeug.local import LocalProxy

flask_app = Flask(__name__)


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

