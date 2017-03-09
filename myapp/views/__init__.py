#!/usr/bin/python -B
import flask
import httplib
from functools import wraps
from myapp.models import Session
from myapp.models.auth import InvalidCredentials, check_password


class Permissions(object):
    """
    This class currently just serves as a namespace for permission names.
    """
    # allows viewing basic information of a report
    PERMISSION_VIEW_REPORT = "view_report"
    # allows viewing all information of a report
    PERMISSION_VIEW_FULL_REPORT = "view_full_report"


def get_credentials():
    try:
        authorization = flask.request.form if hasattr(flask.request, 'form') and flask.request.form else flask.request.authorization
        return dict(username=authorization['username'], password=authorization['password'])
    except TypeError:
        return None


def verify_credentials(password, password_hash):
    try:
        check_password(password, password_hash)
    except InvalidCredentials:
        flask.abort(httplib.FORBIDDEN, 'Authentication failed')


def pre_check_credentials(must_be_in=False, must_be_out=False):
    def w(f):
        @wraps(f)
        def fwrapper(*args, **dargs):
            if must_be_in and not Session.logged():
                return 'Not logged in', httplib.FORBIDDEN
            elif must_be_out and Session.logged():
                return 'Already logged in ({})'.format(Session.username()), httplib.FORBIDDEN
            creds = get_credentials()
            if not creds:
                return 'Logout failed: no credentials provided', httplib.FORBIDDEN
            if must_be_in:
                verify_credentials(creds['password'], Session.get()['password_hash'])
            fwrapper.credentials = creds
            return f(*args, **dargs)
        return fwrapper
    return w


