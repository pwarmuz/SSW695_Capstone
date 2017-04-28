import string, random
from werkzeug.security import generate_password_hash
from app import mongo_client
import pymongo


def generate_password(pw_length=12, valid_chars=string.ascii_letters + string.digits):
    """ Generate a random password

    :param pw_length: Length of password
    :param valid_chars: Characters allowed in password

    :return: random password

    """
    return "".join(random.choice(valid_chars) for i in range(pw_length))


def create_new_user(email, password=None, is_admin=False):
    """ Create new users

    """
    if password is None:
        password = generate_password()

    password_hash = generate_password_hash(password, method='pbkdf2:sha256:100000', salt_length=16)

    # Insert the users in the DB
    try:
        mongo_client.ssw695.users.insert({"_id": email, "password": password_hash, "is_admin": is_admin, "rating": 3})
    except pymongo.errors.DuplicateKeyError:
        return {"success": False, "message": "Email already exists"}
    return {"success": True, "message": "User created successfully"}


def get_user(email):
    return mongo_client.ssw695.users.find_one({"_id": email})


def current_rating(email):
    """ Retrieve rating for filter """
    user = get_user(email)
    if user is not None:
        user_rating = user.get("rating")
        if user_rating is not None:
            return user_rating
    return "User Not Rated"
