# coding=utf-8
""" '/books' Views """
from flask import Blueprint, render_template, abort
import tools

blueprint = Blueprint('books', __name__, url_prefix="/books")


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


