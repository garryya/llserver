import flask


auth_view = flask.Blueprint('auth', __name__)


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
    return "TODO: Implement login"


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
    return "TODO: Implement whoami"


@auth_view.route('/logout', methods=['POST'])
def logout():
    """
    Logout the current user.

    URL: /auth/logout
    """
    return "TODO: Implement logout"