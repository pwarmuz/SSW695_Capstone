from flask import Blueprint, render_template, abort, jsonify

import tools
blueprint = Blueprint('listing', __name__)


@blueprint.route('/listing/')
def get_listing():
    """ get first 10 entries of book listing
    """
    results = tools.get_ten_list()
    return render_template('/listing/listing.html', listing=results)


