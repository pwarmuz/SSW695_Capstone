#!/usr/bin/env python

""" Run Web Server """
import sys
import signal
from app import flask_app

""" This fixes the slow Ctrl+C python interpreter """
signal.signal(signal.SIGINT, signal.SIG_DFL)


def local_server():
    """ Launch local server
        DEBUG is set in private configuration
    """
    flask_app.run(host="127.0.0.1", port=5000, threaded=True)
    sys.exit(1)


if __name__ == "__main__":
    local_server()
