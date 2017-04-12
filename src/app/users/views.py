
from flask import Blueprint, request, redirect, render_template, url_for, flash, session, current_app
from flask_login import login_user, logout_user
from manager import User
from app import mongo_client
import tools

blueprint = Blueprint('Users', __name__)


@blueprint.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    r = mongo_client.ssw695.users.find_one({"email": email},
                                           {'_id': False})

    if r is not None:
        return 'already signed up!'


    print 'adding email: {0} password: {1}'.format(email, password)

    ret = tools.create_new_user(email=email, 
                                password=password)

    if ret.get('success') == True:
        user = User(email)
        login_user(user)

    return redirect(url_for('home'))


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
