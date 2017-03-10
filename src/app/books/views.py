# coding=utf-8
""" '/books' Views """
from flask import Blueprint, render_template, abort
import tools

blueprint = Blueprint('books', __name__, url_prefix="/books")

'''
@blueprint.route('/')
def display_courses_by_departments():
    """ Display Courses By Departments """

    # TODO: MongoDB Exceptions
    departments = tools.get_courses_by_departments()

    return render_template('courses/by_department.html', departments=departments)
'''


@blueprint.route('/<isbn>')
def display_book(isbn):
    """ Display a specific book based on isbn Page
    :param isbn: isbn Number (10-digit)
    """
    # TODO: MongoDB Exceptions
    book = tools.get_books(isbn)

    if book is None:
        abort(404)

    return render_template('books/book_isbn.html', book=book, isbn=isbn)


