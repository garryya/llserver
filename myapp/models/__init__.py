#!/usr/bin/python -B
from time import time
import sqlite3

#TODO logging
#TODO remove cred check copypast
#TODO session timeout
#TODO use flas session, maybe...
#TODO configuration file --> flask conf
#TODO exception handling
#TODO multiple-session, concurrency
#TODO HTTP error constants (flask.ext.api?)
#TODO differentiate auth errors
#TODO SQLAlchemy, ORM
#TODO testing: classes, group by functionality (login, logout etc.)
#TODO testing: more mocking


class Session:
    __user = None

    @staticmethod
    def is_valid():
        return Session.__user

    @staticmethod
    def logged():
        return Session.is_valid()

    @staticmethod
    def get(fields = None):
        user = Session.__user
        if fields:
            user = dict((k,v) for k,v in user.items() if k in fields)
        return user

    @staticmethod
    def set(user):
        user['.created'] = time()
        Session.__user = user

    @staticmethod
    def unset():
        Session.__user = None

    @staticmethod
    def username():
        return Session.__user['username'] if Session.logged() else None

    @staticmethod
    def is_user(user):
        return Session.logged() and Session.username() == user


class DB:
    def __init__(self, dbfile, timeout=2):
        self.dbfile = dbfile
        self.timeout = timeout

    def _connect(self):
        return sqlite3.connect(self.dbfile, timeout=self.timeout)

    def _excecute(self, sql):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            r = cursor.fetchone()
            columns = [str(c[0]) for c in cursor.description]
            return dict(zip(columns, [v for v in r])) if r and columns else None

    def get_user(self, username):
        sql = 'select * from account join account_permission using(account_id) ' \
              'join permission using (permission_id) ' \
              'where username="{}"'.format(username)
        return self._excecute(sql)