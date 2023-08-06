import hashlib

from pytest import fixture, raises
from tornado.web import HTTPError


from ..auth import TokenExchangeAuthenticator

from .mocks import setup_oauth_mock


def user_model(email):
    """Return a user model"""
    return {'sub': hashlib.md5(email.encode()).hexdigest(), 'email': email, 'hd': email.split('@')[1], 'verified_email': True}


def openid_configuration(request):
    """Mock response from .well-known/openid-configuration"""
    return {
       "issuer": "http://mydomain.com/auth/realms/ssb",
       "authorization_endpoint": "http://mydomain.com/auth/realms/ssb/protocol/openid-connect/auth",
       "token_endpoint": "http://mydomain.com/auth/realms/ssb/protocol/openid-connect/token",
       "userinfo_endpoint": "http://mydomain.com/auth/realms/ssb/protocol/openid-connect/userinfo",
       "end_session_endpoint": "http://mydomain.com/auth/realms/ssb/protocol/openid-connect/logout",
    }


@fixture
def google_client(client):
    setup_oauth_mock(
        client,
        host=['mydomain.com'],
        access_token_path='/openid-connect/token',
        user_path='/openid-connect/userinfo',
    )
    client.add_host('mydomain.com', [
        ('/auth/realms/ssb/.well-known/openid-configuration', openid_configuration)
    ])
    return client


async def test_google(google_client):
    authenticator = TokenExchangeAuthenticator(oidc_issuer='http://mydomain.com/auth/realms/ssb/auth/realms/ssb')
    handler = google_client.handler_for_user(user_model('fake@email.com'))
    user_info = await authenticator.authenticate(handler)
    assert sorted(user_info) == ['auth_state', 'name']
    name = user_info['name']
    assert name == 'fake@email.com'
    auth_state = user_info['auth_state']
    assert 'access_token' in auth_state
    assert 'google_user' in auth_state


async def test_google_username_claim(google_client):
    authenticator = TokenExchangeAuthenticator(oidc_issuer='http://mydomain.com/auth/realms/ssb/auth/realms/ssb')
    handler = google_client.handler_for_user(user_model('fake@email.com'))
    user_info = await authenticator.authenticate(handler)
    assert sorted(user_info) == ['auth_state', 'name']
    name = user_info['name']
    assert name == '724f95667e2fbe903ee1b4cffcae3b25'


async def test_hosted_domain(google_client):
    authenticator = TokenExchangeAuthenticator(oidc_issuer='http://mydomain.com/auth/realms/ssb/auth/realms/ssb', hosted_domain=['email.com'])
    handler = google_client.handler_for_user(user_model('fake@email.com'))
    user_info = await authenticator.authenticate(handler)
    name = user_info['name']
    assert name == 'fake'

    handler = google_client.handler_for_user(user_model('notallowed@notemail.com'))
    with raises(HTTPError) as exc:
        name = await authenticator.authenticate(handler)
    assert exc.value.status_code == 403


async def test_multiple_hosted_domain(google_client):
    authenticator = TokenExchangeAuthenticator(oidc_issuer='http://mydomain.com/auth/realms/ssb/auth/realms/ssb', hosted_domain=['email.com', 'mycollege.edu'])
    handler = google_client.handler_for_user(user_model('fake@email.com'))
    user_info = await authenticator.authenticate(handler)
    name = user_info['name']
    assert name == 'fake@email.com'

    handler = google_client.handler_for_user(user_model('fake2@mycollege.edu'))
    user_info = await authenticator.authenticate(handler)
    name = user_info['name']
    assert name == 'fake2@mycollege.edu'

    handler = google_client.handler_for_user(user_model('notallowed@notemail.com'))
    with raises(HTTPError) as exc:
        name = await authenticator.authenticate(handler)
    assert exc.value.status_code == 403

