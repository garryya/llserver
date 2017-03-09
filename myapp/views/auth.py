#!/usr/bin/python -B
import flask
import httplib
from myapp.views import pre_check_credentials, verify_credentials
from myapp.models import Session, DB


auth_view = flask.Blueprint('auth', __name__)

db = DB('data/credentials.db')



@auth_view.route('/login', methods=['POST'])
@pre_check_credentials(must_be_out=True)
def login():
    """
    Log in a user.

    If successful, create a session for this user.

    URL: /auth/login

    GET Parameters:

    - username
    - password

    For verifying a password, use `models.check_password()`
    Current user accounts are stored in the `account` table
    in `data/credentials.db`. This is an sqlite file,
    you can access it with the python sqlite3 module.
    For testing, the plaintext passwords of the current
    users are in `data/passwords.txt`.

    Return: "OK" on success. On failure, return HTTP 403.
    """
    user = db.get_user(login.credentials['username'])
    if not user:
        return 'Login failed: user {} not found'.format(login.credentials['username']), httplib.FORBIDDEN
    verify_credentials(login.credentials['password'], user['password_hash'])
    Session.set(user)
    return "OK"


@auth_view.route('/whoami', methods=['GET'])
def whoami():
    """
    Return identity of the currently logged in user.

    URL: /auth/whoami

    Returns JSON dictionary containing fields:

    - username
    - first_name
    - last_name

    This information is in the `account` table of
    data/credentials.db.

    If user is not logged in return HTTP 403
    """
    if not Session.logged():
        return 'Not logged in', httplib.FORBIDDEN
    user = Session.get(fields=['username', 'first_name', 'last_name'])
    return flask.jsonify(user)


@auth_view.route('/logout', methods=['POST'])
@pre_check_credentials(must_be_in=True)
def logout():
    """
    Logout the current user.

    URL: /auth/logout
    """
    if not Session.is_user(logout.credentials['username']):
        return 'Only {} can logout'.format(Session.username()), httplib.FORBIDDEN
    verify_credentials(logout.credentials['password'], Session.get()['password_hash'])
    Session.unset()
    return "Logged out"
