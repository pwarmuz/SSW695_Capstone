from flask import Blueprint, render_template, abort, jsonify

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

@blueprint.route('/api/courses/')
def get_courses():

    courses = list(tools.get_courses_by_departments())

    for course in courses:
        children = course.get('children') 
        for child in children:
            letter = child.get('a_attr').get('data-letter')
            number = child.get('a_attr').get('data-number')
            #books = list(tools.get_books_by_course(letter, number))
            print books
            #child.get('a_attr')['books'] = books

    return jsonify(results=courses)

@blueprint.route('/api/books/')
def get_books():

    return jsonify(results=tools.get_books())
