__version__ = '0.2'

import os

from flask import Flask, render_template, request, redirect, url_for

from werkzeug.local import LocalProxy
from context import get_db
from flask_track_usage import TrackUsage
from flask_track_usage.storage.mongo import MongoStorage

try:
    import config_private as config
except ImportError:
    import config_public as config


flask_app = Flask(__name__)
flask_app.config.from_object(config.BaseConfig)
mongo_client = LocalProxy(get_db)


print('Stevens Book Marketplace Version: ' + __version__)

import courses
flask_app.register_blueprint(courses.blueprint)

import book
from book import tools
flask_app.register_blueprint(book.blueprint)


import listing
flask_app.register_blueprint(listing.blueprint)

import users
flask_app.register_blueprint(users.blueprint)
users.login_manager.init_app(flask_app)

with flask_app.app_context():
    flask_app.session_interface = users.SessionInterface(mongo_client)

# LOCAL CONSOLE TESTING
# analytics = TrackUsage(flask_app, PrintStorage())


analytics = TrackUsage(flask_app, MongoStorage(database='ssw695',
                                               collection='analytics',
                                               host=flask_app.config.get("MONGO_HOST"),
                                               port=flask_app.config.get("MONGO_PORT"),
                                               username=flask_app.config.get("MONGO_USER"),
                                               password=flask_app.config.get("MONGO_PASSWORD"),
                                               auth_db=flask_app.config.get("MONGO_AUTH_DB"),
                                               auth_mechanism=flask_app.config.get("MONGO_AUTH_MECH")))

analytics.include_blueprint(courses.blueprint)
analytics.include_blueprint(book.blueprint)
analytics.include_blueprint(listing.blueprint)
analytics.include_blueprint(users.blueprint)


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


@analytics.include
@flask_app.route('/')
def home():
    results = listing.views.get_listing()
    return render_template('index.html', listing=results)


@analytics.include
@flask_app.route('/about')
def about():
    return render_template('about.html')


@analytics.include
@flask_app.route('/contact')
def contact():
    return render_template('contact.html')


@analytics.include
@flask_app.route('/profile')
def profile():
    # TODO: Temporary profile access to be deleted
    return render_template('profile.html')


@flask_app.route('/submit_form', methods=['POST'])
def submit_form():
    username = request.form['username']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    print('contact form message from: {0} and email: {1} and subject: {2} and message {3}' .format(username, email, subject, message))
    return redirect(url_for('home'))


@analytics.include
@flask_app.route('/', methods=['POST'])
def jumbo_search():
    search_input = request.form['jumbo-search']

    if book.tools.validate_by_isbn(search_input):
        return redirect('/book/' + search_input)
    
    book_results = book.tools.search_titles(search_input) 
    course_results = courses.tools.search_courses(search_input)

    return render_template('search_results.html', search_input=search_input, book_results=book_results, course_results=course_results)
