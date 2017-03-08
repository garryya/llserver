import flask
from myapp.models import Session, DB
from myapp.models import auth
import httplib
from functools import wraps

auth_view = flask.Blueprint('auth', __name__)

db = DB('data/credentials.db')


def get_credentials():
    try:
        authorization = flask.request.form if hasattr(flask.request, 'form') and flask.request.form else flask.request.authorization
        return dict(username=authorization['username'], password=authorization['password'])
    except TypeError:
        return None



def pre_check_credentials(must_be_in=False, must_be_out=False):
    def w(f):
        @wraps(f)
        def fwrapper():
            if must_be_in and not Session.logged():
                return 'Not logged in', httplib.OK
            elif must_be_out and Session.logged():
                return 'Already logged in ({})'.format(Session.username()), httplib.FORBIDDEN
            creds = get_credentials()
            if not creds:
                return 'Logout failed: no credentials provided', httplib.FORBIDDEN
            fwrapper.credentials = creds
            return f()
        return fwrapper
    return w


def verify_credentials(password, password_hash):
    try:
        auth.check_password(password, password_hash)
    except auth.InvalidCredentials:
        flask.abort(httplib.FORBIDDEN, 'Login failed: bad password')


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
