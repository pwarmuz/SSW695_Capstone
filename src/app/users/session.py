"""
Server-side sessions with MongoDB (pymongo)

References:
    http://flask.pocoo.org/snippets/51/
    http://flask.pocoo.org/snippets/109/
    http://flask.pocoo.org/snippets/110/
    http://thecircuitnerd.com/flask-login-tokens/
    http://nullege.com/codes/show/src@a@b@abilian-core-0.1.4@abilian@services@auth@views.py/27/flask.ext.login.user_logged_in
"""

from datetime import datetime, timedelta
from uuid import uuid4
from flask import current_app
from flask.sessions import SessionInterface, SessionMixin
from itsdangerous import Signer, BadSignature
from werkzeug.datastructures import CallbackDict


class MySession(CallbackDict, SessionMixin):
    @classmethod
    def new(cls):
        return cls(sid=str(uuid4()))

    def __init__(self, initial=None, sid=None):
        CallbackDict.__init__(self, initial)
        self.sid = sid
        self.modified = False

    def clear(self):
        current_app.session_interface.store.delete_one({'_id': self.sid})
        super(MySession, self).clear()


class MySessionInterface(SessionInterface):
    session_class = MySession

    def __init__(self, client, db='ssw695', collection='sessions'):
        self.store = client[db][collection]
        self.store.create_index([("expireAt", 1)], expireAfterSeconds=0)

    @staticmethod
    def get_signer(app):
        if not app.secret_key:
            return None
        return Signer(app.secret_key)

    def open_session(self, app, request):
        s = self.get_signer(app)
        if s is None:
            return None
        signed_sid = request.cookies.get(app.session_cookie_name)
        if signed_sid:
            try:
                sid = s.unsign(signed_sid)
            except BadSignature:
                pass
            else:
                stored_session = self.store.find_one({'_id': sid})
                if stored_session and (stored_session.get('expireAt') > datetime.utcnow()):
                    return self.session_class(initial=stored_session.get('data', {}), sid=sid)
                else:
                    self.store.delete_many({'_id': sid})
        return self.session_class.new()

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)

        if not session:
            response.delete_cookie(app.session_cookie_name, domain=domain, path=path)
            return

        # Push Back Expiration
        if self.get_expiration_time(app, session):
            expires = self.get_expiration_time(app, session)
        else:
            expires = datetime.utcnow() + timedelta(days=10)

        self.store.update({'_id': session.sid},
                          {'data': session,
                           'last_accessed': datetime.utcnow(),
                           'expireAt': expires}, True)

        signed_sid = self.get_signer(app).sign(session.sid)

        response.set_cookie(app.session_cookie_name,
                            signed_sid,
                            expires=expires,
                            httponly=self.get_cookie_httponly(app),
                            domain=domain,
                            path=path,
                            secure=self.get_cookie_secure(app))
