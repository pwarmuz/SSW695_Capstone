from flask import Blueprint, render_template

import tools
blueprint = Blueprint('categories', __name__, url_prefix="/categories")


@blueprint.route('/')
def display_categories():
    return render_template('categories/display_categories.html', departments=tools.get_courses_by_departments())


@blueprint.route('/<category>')
def display_category(category):
   return "display category here"