#!/usr/bin/env python

""" Run Web Server """
import sys
import config_public as config
from app import flask_app


def local_server():
    """ Launch local server """
    flask_app.config.from_object(config.BaseConfig)
    flask_app.run(host="127.0.0.1", port=5000, threaded=True, debug=True)
    sys.exit(1)


if __name__ == "__main__":
    local_server()
