import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OIDC_CLIENT_SECRETS = 'client_secrets.json'
OIDC_ID_TOKEN_COOKIE_SECURE = False
OIDC_REQUIRE_VERIFIED_EMAIL = True
OIDC_SCOPES = ['openid', 'email', 'profile']
OIDC_ID_TOKEN_COOKIE_TTL = 30
OIDC_ID_TOKEN_COOKIE_NAME = 'oidc_id_token'
OIDC_USER_INFO_ENABLED = True
OIDC_CALLBACK_ROUTE = '/callback'
# OIDC_INTROSPECTION_AUTH_METHOD = 'bearer'
