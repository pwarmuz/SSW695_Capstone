# coding=utf-8
""" '/books' Views """
from flask import Blueprint, render_template, abort
import tools

blueprint = Blueprint('books', __name__, url_prefix="/books")


def validate_by_isbn(isbn):
    """ Validates the ISBN
    :param isbn: isbn Number (10-digit)
    """
    # Prevents users from entering none digit values
    if not isbn.isdigit():
        return False

    # TODO: MongoDB Exceptions
    book = tools.get_book(isbn)

    if not book:
        return False

    return True


@blueprint.route('/<isbn>')
def display_book(isbn):
    """ Display a specific book based on isbn Page
    :param isbn: isbn Number (10-digit)
    """
    # Prevents users from entering none digit values
    if not isbn.isdigit():
        abort(404)

    # TODO: MongoDB Exceptions
    book = tools.get_book(isbn)

    if not book:
        abort(404)

    return render_template('books/book_isbn.html', book=book, isbn=isbn)


