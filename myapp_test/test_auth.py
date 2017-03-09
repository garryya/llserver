import pytest
import httplib
import httplib2
import base64
import json

http = httplib2.Http()
root_address = 'http://127.0.0.1:8080/'

good_user = {
    "first_name": "Joe",
    "last_name": "Admin",
    "username": "jadmin@lastline.com",
    "password": "aio1jda61SJh",
}

def httpreq(uri, user=None, password=None, method='GET'):
    address = root_address + uri
    print('HTTP request: {} {} user={} password={}...'.format(method, address, user, password))
    headers = None
    if user and password:
        # http.add_credentials(user, password)
        headers = {'Authorization':'Basic '+base64.b64encode(user+':'+password)}
    content = http.request(address, method=method, headers=headers)
    print('\t\t--> {}'.format(content))
    return content[0], content[1]


def isstatus(r, s):
    return int(r['status']) == s


def isok(r):
    return isstatus(r, httplib.OK)


@pytest.fixture(scope='function')
def restart():
    httpreq('auth/logout', user=good_user['username'], password=good_user['password'], method='POST')
    pass


def test_0(restart):
    response, _ = httpreq('')
    assert isok(response)


def test_whoami___not_logged():
    r, _ = httpreq('auth/whoami')
    assert isstatus(r, httplib.FORBIDDEN)


# LOGIN


def test_login___no_credentials():
    r, data = httpreq('auth/login', method='POST')
    assert isstatus(r, httplib.FORBIDDEN)


def test_login___bad_user():
    r, data = httpreq('auth/login', user='BADUSER', method='POST')
    assert isstatus(r, httplib.FORBIDDEN)


def test_login___bad_password():
    r, data = httpreq('auth/login', user=good_user['username'], password='BADPASS', method='POST')
    assert isstatus(r, httplib.FORBIDDEN)


def test_login___good(restart):
    r, data = httpreq('auth/login', user=good_user['username'], password=good_user['password'], method='POST')
    assert isstatus(r, httplib.OK)
    r, data = httpreq('auth/whoami')
    assert isstatus(r, httplib.OK)
    user = json.loads(data)
    assert user['username'] == good_user['username']


# LOGOUT

def test_logout___no_credentials():
    r, data = httpreq('auth/logout', method='POST')
    assert isstatus(r, httplib.FORBIDDEN)


def test_logout___wrong_user():
    r, data = httpreq('auth/logout', user='jsmith@lastline.com', method='POST')
    assert isstatus(r, httplib.FORBIDDEN)


def test_logout___bad_user():
    r, data = httpreq('auth/logout', user='BADUSER', method='POST')
    assert isstatus(r, httplib.FORBIDDEN)


def test_logout___bad_password():
    r, data = httpreq('auth/logout', user=good_user['username'], password='BADPASS', method='POST')
    assert isstatus(r, httplib.FORBIDDEN)


def test_logout___good():
    r, data = httpreq('auth/logout', user=good_user['username'], password=good_user['password'], method='POST')
    assert isstatus(r, httplib.OK)
    r, data = httpreq('auth/whoami')
    assert isstatus(r, httplib.FORBIDDEN)


def test_logout___not_loggedin(restart):
    r, data = httpreq('auth/logout', method='POST')
    assert isstatus(r, httplib.OK) and 'not logged' in data.lower()



