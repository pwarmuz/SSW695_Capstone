from flask import Blueprint, render_template, abort, jsonify

import tools
blueprint = Blueprint('listing', __name__)


def get_listing():
    """ get first 10 entries of books listing
    This is redundant as it just returns what was previously created in tools....
    """
    return tools.get_ten_list()


