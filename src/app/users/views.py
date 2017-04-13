
from flask import Blueprint, request, redirect, render_template, url_for, flash, session, current_app, json
from flask_login import login_user, logout_user
from manager import User
from app import mongo_client

blueprint = Blueprint('Users', __name__)


#@blueprint.route('/signup', methods=['POST'])
#def signup():
#    name = request.form.get('name')
#    email = request.form.get('email')
#    password = request.form.get('password')
#
#    r = mongo_client.ssw695.users.find_one({"email": email},
#                                           {'_id': False})
#
#    if r is not None:
#        return 'already signed up!'
#
#    user = {'name': name,
#            'email': email,
#            'password': password}#
#
#    mongo_client.ssw695.users.insert_one(user)
#
#   session['username'] = name
#    return redirect(url_for('home'))


@blueprint.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User(email)
    if user is not None and user.check_password(password):
        login_user(user)
    else:
        flash("Invalid username or password", category="error")
    return redirect(url_for('home'))


@blueprint.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))


@blueprint.route('/rate', methods=['POST'])
def rate():
    rating = request.form['rating_val']
    User.set_rating(rating)

