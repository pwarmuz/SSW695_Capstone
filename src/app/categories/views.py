from flask import Blueprint, render_template, abort

import tools
blueprint = Blueprint('categories', __name__)


@blueprint.route('/departments/')
def departments():
    return render_template('categories/departments.html', departments=tools.get_courses_by_departments())


@blueprint.route('/course/<letter>-<number>')
def course(letter, number):
    course = tools.get_course(letter, number)

    if course is None:
        abort(404)

    return render_template('categories/course.html', course=course)
