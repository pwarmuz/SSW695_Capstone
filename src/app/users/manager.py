from datetime import date
from app import mongo_client, flask_app
from werkzeug.security import check_password_hash
from flask_login import UserMixin, LoginManager
from bson.objectid import ObjectId

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

    def list_book(self, isbn, list_price, condition):
        """
        Set the sellers of an isbn book item onto listing page
        """
        date_listed = str(date.today())
        date_sold = str(date.today())
        seller_rating = self._collection.find_one({"_id": self.id}, {"_id": 0, "rating": 1})
        # valid transaction phases are listed, negotiation, sold
        mongo_client.ssw695.listing.insert({"seller": self.id, "buyer": "none",
                                            "seller_rating": seller_rating, "buyer_rating": 0,
                                            "date_listed": date_listed, "date_sold": date_sold,
                                            "isbn": isbn, "condition": condition,
                                            "price": float(list_price), "transaction": "listed"}, {"unique": 'true'})

    def list_my_books_listed(self):
        """
        lists the books listed
        """
        return list(mongo_client.ssw695.listing.find({"seller": self.id, "transaction": "listed"}))

    def count_my_books_listed(self):
        """
        counts the books listed
        """
        return mongo_client.ssw695.listing.find({"seller": self.id, "transaction": "listed"}).count()

    def list_my_buyer_negotiation(self):
        """
        lists the books as a buyer in negotiation
        """
        return list(mongo_client.ssw695.listing.find({"buyer": self.id, "transaction": "negotiation"}))

    def list_my_seller_negotiation(self):
        """
        lists the books as a seller in negotiation
        """
        return list(mongo_client.ssw695.listing.find({"seller": self.id, "transaction": "negotiation"}))

    def count_my_books_negotiation(self):
        """
        counts the books in negotiation
        """
        return mongo_client.ssw695.listing.find({"buyer": self.id, "transaction": "negotiation"}).count() + mongo_client.ssw695.listing.find({"seller": self.id, "transaction": "negotiation"}).count()

    def list_my_books_sold(self):
        """
        lists the books sold
        """
        return list(mongo_client.ssw695.listing.find({"seller": self.id, "transaction": "sold"})) + list(mongo_client.ssw695.listing.find({"buyer": self.id, "transaction": "sold"}))

    def count_my_books_sold(self):
        """
        counts the books sold
        """
        return mongo_client.ssw695.listing.find({"seller": self.id, "transaction": "sold"}).count()

    def buy_into_negotiation(self, transaction):
        """
        The user is buying into the negotiation phase
        """
        mongo_client.ssw695.listing.update({"_id": ObjectId(str(transaction))}, {"$set": {"buyer": self.id, "buyer_rating": self.rating, "transaction": "negotiation"}})

    def close_transaction(self, transaction_id, transaction_state):
        if transaction_state == "Cancel":
            mongo_client.ssw695.listing.update({"_id": ObjectId(str(transaction_id))}, {"$set": {"transaction": "listed"}})
            return
        other = mongo_client.ssw695.listing.find_one({"_id": ObjectId(str(transaction_id))}, {"_id": 0, "buyer": 1, "seller": 1})
        if other['buyer'] == self.id:
            mongo_client.ssw695.users.update({"_id": str(other['seller'])}, {"$set": {"rating": int(transaction_state)}})
        if other['seller'] == self.id:
            mongo_client.ssw695.users.update({"_id": str(other['buyer'])}, {"$set": {"rating": int(transaction_state)}})
        mongo_client.ssw695.listing.update({"_id": ObjectId(str(transaction_id))}, {"$set": {"transaction": "sold"}})

    @property
    def document(self):
        return self._collection.find_one({"_id": self.id})

    @property
    def rating(self):
        return self.document.get("rating")

    def check_password(self, password):
        doc = self.document
        return check_password_hash(self.document.get('password'), password) if doc else None
