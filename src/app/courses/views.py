# coding=utf-8
""" '/courses' Views """
from flask import Blueprint, render_template, abort
import tools

blueprint = Blueprint('courses', __name__, url_prefix="/courses")


@blueprint.route('/')
def display_all_courses():
    """ Display All Courses By Departments """

    # TODO: MongoDB Exceptions
    departments = tools.get_courses_by_departments()

    return render_template('courses/by_department.html', departments=departments)


@blueprint.route('/<letter>-<number>')
def display_course(letter, number):
    """ Display Course Page
    :param letter: Course Letters
    :param number: Course Numbers
    """
    # TODO: MongoDB Exceptions
    course = tools.get_course(letter, number)

    if course is None:
        abort(404)

    # TODO: MongoDB Exceptions
    books = tools.get_books_by_course(letter, number)

    return render_template('courses/course.html', course=course, books=books)
