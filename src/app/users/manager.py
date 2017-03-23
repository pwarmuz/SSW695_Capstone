from app import mongo_client, flask_app
from werkzeug.security import check_password_hash
from flask_login import UserMixin, LoginManager

login_manager = LoginManager()
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(userid):
    """
    Flask-Login user_loader callback.
    The user_loader function asks this function to get a User Object or return
    None based on the userid.
    The userid was stored in the users environment by Flask-Login.
    user_loader stores the returned User object in current_user during every
    flask request.
    """
    return User.get(userid)


class User(UserMixin):
    """
    User Class for flask-Login
    """

    with flask_app.app_context():
        _collection = mongo_client.ssw695.users

    def __init__(self, userid):
        self.id = userid

    @classmethod
    def get(cls, id):
        """
        Static method to search the database and see if userid exists.  If it
        does exist then return a User Object.  If not then return None as
        required by Flask-Login.
        """
        doc = cls._collection.find_one({"_id": id})
        return User(id) if doc is not None else None

    @property
    def document(self):
        return self._collection.find_one({"_id": self.id})

    def check_password(self, password):
        doc = self.document
        return check_password_hash(self.document.get('password'), password) if doc else None
