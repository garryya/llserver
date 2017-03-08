import pytest
import httplib
import httplib2


http = httplib2.Http()
root_address = 'http://127.0.0.1:8080/'

good_user = {
    "first_name": "Joe",
    "last_name": "Admin",
    "username": "jadmin@lastline.com",
    "password": "aio1jda61SJh",
}

def httpreq(uri, user=None, password=None, method='GET'):
    if user and password:
        http.add_credentials(user, password)
    content = http.request(root_address + uri, method=method)
    return content[0]


def isstatus(r, s):
    return int(r['status']) == s


def isok(r):
    return isstatus(r, httplib.OK)


@pytest.fixture(scope='function')
def nullify():
    #content = httpreq('auth/logout', method='POST')
    pass


def test_0():
    response = httpreq('')
    assert isok(response)


def test_whoami___not_logged():
    r = httpreq('auth/whoami')
    assert isstatus(r, httplib.FORBIDDEN)


def test_login___no_credentials():
    r = httpreq('auth/login')
    assert isstatus(r, httplib.FORBIDDEN)


def test_login___bad_user():
    r = httpreq('auth/login', user='BADUSER')
    assert isstatus(r, httplib.FORBIDDEN)


def test_login___bad_password():
    r = httpreq('auth/login', user=good_user['username'], password='BADPASS')
    assert isstatus(r, httplib.FORBIDDEN)


def test_login___good():
    r = httpreq('auth/login', user=good_user['username'], password=good_user['password'])
    assert isstatus(r, httplib.OK)


def test_whoami__good():
    r = httpreq('auth/whoami')
    assert isstatus(r, httplib.OK)



