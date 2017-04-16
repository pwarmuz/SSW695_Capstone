from datetime import date
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


def poll_user_rating(user_name):
    """
    polls the usernames of a listing to get rating
    """
    return mongo_client.ssw695.listing.find_one({"_id": user_name}, {"_id": 0, "rating": 1})


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

    def set_rating(self, rating):
        """
        Set rating for user
        """
        mongo_client.ssw695.users.update({"_id": str(self.id)}, {"$set": {"rating": rating}})

    def list_book(self, isbn, list_price):
        """
        Set the sellers of an isbn books item onto listing page
        """
        list_date = str(date.today())
        seller_rating = self._collection.find_one({"_id": self.id}, {"_id": 0, "rating": 1})
        mongo_client.ssw695.listing.insert({"seller": self.id, "seller_rating": seller_rating, "isbn": isbn, "date": list_date, "price": float(list_price)}, {"unique": 'true'})

    def list_my_books_listed(self):
        """
        lists the users items sold
        """
        return list(mongo_client.ssw695.listing.find({"seller": self.id}))

    def count_my_books_listed(self):
        """
        counts the users items sold
        """
        return len(list(mongo_client.ssw695.listing.find({"seller": self.id})))

    def list_my_books_sold(self):
        """
        lists the users items sold
        """
        return list(mongo_client.ssw695.sold.find({"seller": self.id}))

    def count_my_books_sold(self):
        """
        counts the users items sold
        """
        return len(list(mongo_client.ssw695.sold.find({"seller": self.id})))

    @property
    def document(self):
        return self._collection.find_one({"_id": self.id})

    @property
    def rating(self):
        return self.document.get("rating")

    def check_password(self, password):
        doc = self.document
        return check_password_hash(self.document.get('password'), password) if doc else None
