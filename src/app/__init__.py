import os

from flask import Flask, render_template, jsonify, abort, request
from werkzeug.local import LocalProxy

flask_app = Flask(__name__)



@flask_app.route('/')
def home():
    return render_template('index.html')


@flask_app.route('/bootstrap_info')
def print_bootstrap_info():
    return "We will be using bootstrap 3.3.7"
