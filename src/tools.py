from app import flask_app
from app.users.tools import create_new_user
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('--add_user', nargs=2)

if __name__ == '__main__':
    args = parser.parse_args()
    with flask_app.app_context():
        if args.add_user is not None:
            print "Attempting to add user:",
            print create_new_user(args.add_user[0], args.add_user[1])
