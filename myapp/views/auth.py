import flask
from myapp.models import Session, DB
from myapp.models import auth

auth_view = flask.Blueprint('auth', __name__)


db = DB('data/credentials.db')


@auth_view.route('/login', methods=['POST'])
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
    authorization = flask.request.form if hasattr(flask.request, 'form') and flask.request.form else flask.request.authorization
    username = authorization['username']
    password = authorization['password']
    user = db.get_user(username)
    if not user:
        return 'Login failed: user {} not found'.format(username), 403
    try:
        auth.check_password(password, user['password_hash'])
    except auth.InvalidCredentials:
        return 'Login failed: bad password', 403
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
        return 'Not logged in', 403
    user = Session.get(fields=['username', 'first_name', 'last_name'])
    return flask.jsonify(user)


@auth_view.route('/logout', methods=['POST'])
def logout():
    """
    Logout the current user.

    URL: /auth/logout
    """
    if not Session.logged():
        return 'Not logged in', 403
    Session.unset()
    return "Logged out"