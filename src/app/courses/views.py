from flask import Blueprint, render_template, abort

import tools
blueprint = Blueprint('courses', __name__)


@blueprint.route('/courses/')
def display_courses_by_departments():
    """ Display Courses By Departments """
    # TODO: MongoDB Exceptions
    departments = tools.get_courses_by_departments()
    return render_template('courses/by_department.html', departments=departments)


@blueprint.route('/courses/<letter>-<number>')
def display_course(letter, number):
    """ Display Course Page
    :param letter: Course Letters
    :param number: Course Numbers
    """
    # TODO: MongoDB Exceptions
    course = tools.get_course(letter, number)

    if course is None:
        abort(404)

    return render_template('courses/course.html', course=course)
