__version__ = '0.5'

import os

from flask import Flask, render_template, jsonify, request, redirect, url_for, session

from werkzeug.local import LocalProxy
from context import get_db
from flask_track_usage import TrackUsage
from flask_track_usage.storage.mongo import MongoPiggybackStorage

try:
    import config_private as config
except ImportError:
    import config_public as config

from flask_login import current_user
from flask import abort

flask_app = Flask(__name__)
flask_app.config.from_object(config.BaseConfig)
mongo_client = LocalProxy(get_db)

print('Stevens Book Marketplace Version: ' + __version__)

import courses

flask_app.register_blueprint(courses.blueprint)

import books

flask_app.register_blueprint(books.blueprint)
flask_app.jinja_env.filters['isbn_to_title'] = books.tools.isbn_to_title


import users

flask_app.register_blueprint(users.blueprint)
users.login_manager.init_app(flask_app)
flask_app.jinja_env.filters['current_rating'] = users.tools.current_rating

with flask_app.app_context():
    flask_app.session_interface = users.SessionInterface(mongo_client)
    analytics = TrackUsage(flask_app, MongoPiggybackStorage(mongo_client['ssw695']['analytics']))

analytics.include_blueprint(courses.blueprint)
analytics.include_blueprint(books.blueprint)
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
    search_input = request.args.get('search', "").strip()
    if search_input != "":

        if books.tools.validate_by_isbn(search_input):
            return redirect(url_for("books.display_book", isbn=search_input))

        return render_template('index.html',
                               search_input=search_input,
                               books=books.tools.search_titles(search_input),
                               courses=courses.tools.search_courses(search_input))

    return render_template('index.html',
                           books=list(books.tools.get_top_books()),
                           courses=list(courses.tools.get_top_courses()))




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
    my_listed = current_user.list_my_books_listed()
    my_listed_count = current_user.count_my_books_listed()
    buyer_negotiation = current_user.list_my_buyer_negotiation()
    seller_negotiation = current_user.list_my_seller_negotiation()
    my_negotiation_count = current_user.count_my_books_negotiation()
    my_sold = current_user.list_my_books_sold()
    my_sold_count = current_user.count_my_books_sold()
    return render_template('profile.html', my_listed=my_listed, my_listed_count=my_listed_count
                           , buyer_negotiation=buyer_negotiation, seller_negotiation=seller_negotiation, my_negotiation_count=my_negotiation_count
                           , my_sold=my_sold, my_sold_count=my_sold_count)


@flask_app.route('/submit_form', methods=['POST'])
def submit_form():
    username = request.form['username']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    print(
        'contact form message from: {0} and email: {1} and subject: {2} and message {3}'.format(username,
                                                                                                email,
                                                                                                subject,
                                                                                                message))
    return redirect(url_for('home'))


@flask_app.route('/set_seller', methods=['POST'])
def set_seller():
    isbn = session.get('isbn_value', None)
    if books.tools.validate_by_isbn(isbn):
        item_price = request.form['ins_price']
        book_condition = request.form['book_condition']
        current_user.list_book(isbn, item_price, book_condition)
        return jsonify({'item_price': str(item_price)})

    # abort(404)
    return jsonify({'error': 'Failed to list'})


@flask_app.route('/negotiation/', methods=['POST'])
def negotiation():
    transaction_id = request.form['transaction_id']
    transaction_location = request.form['transaction_location']
    transaction_day = request.form['transaction_day']
    transaction_time = request.form['transaction_time']
    current_user.buy_into_negotiation(transaction_id, transaction_location, transaction_day, transaction_time)
    return jsonify({'transaction': str(transaction_id)})


@flask_app.route('/transaction/', methods=['POST'])
def transaction():
    transaction_id = request.form['transaction_id']
    transaction_state = request.form['transaction_state']
    current_user.close_transaction(transaction_id, transaction_state)
    return jsonify({'transaction': str(transaction_id)})


@flask_app.route('/rate', methods=['POST'])
def rate():
    rating = request.form['rating_val']
    current_user.set_rating(rating)
