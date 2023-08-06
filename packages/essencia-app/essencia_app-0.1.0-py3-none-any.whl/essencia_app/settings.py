'''
Settings module
'''
from __future__ import annotations
# import logging
import os
import typing
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
from typesystem import Jinja2Forms
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from authlib.integrations.starlette_client import OAuth

from contextvars import copy_context, ContextVar

cvar_patient = ContextVar('cvar_patient', default=None)
cvar_doctor = ContextVar('cvar_doctor', default=None)
cvar_visit = ContextVar('cvar_visit', default=None)
cvar_subjective = ContextVar('cvar_subjective', default=None)
cvar_objective = ContextVar('cvar_objective', default=None)
cvar_assessment = ContextVar('cvar_assessment', default=None)
cvar_plan = ContextVar('cvar_plan', default=None)

CURRENT_DIR = os.path.join(os.path.dirname(__file__))

ENV_PATH = os.path.join(CURRENT_DIR, '.env')
STATIC_DIR = os.path.join(CURRENT_DIR, 'static')
TEMPORARY_DIR =os.path.join(CURRENT_DIR, 'temp')
TEMPLATES_DIR = os.path.join(CURRENT_DIR, 'templates')


FORMS = Jinja2Forms(package='bootstrap4')
TEMPLATES = Jinja2Templates(directory=TEMPLATES_DIR)
STATIC = StaticFiles(directory=STATIC_DIR, packages=["bootstrap4"])

config = Config(env_file=ENV_PATH)

DEBUG = config('DEBUG', cast=bool, default=False)

# GOOGLE OAUTH
OAUTH_SERVICE = config('OAUTH_SERVICE', cast=str, default='google')
OAUTH_CONF_URL = config('OAUTH_CONF_URL', cast=str, default='https://accounts.google.com/.well-known/openid-configuration')
CLIENT_ID = config('CLIENT_ID', cast=str, default='651932916219-8j5diglh79fucssf0nvql0t06silb7nl.apps.googleusercontent.com')
CLIENT_SECRET = config('CLIENT_SECRET', cast=str, default='CxBFGuwoub-3F8Ly1Sdgcs1y')

# NOSQL DATA
DETA_KEY_TYPING = typing.Union['UserId', str]
DETA_OBJECT_DATA_TYPING = typing.Union[typing.Dict[str, typing.Any], None]
DETA_OBJECT_MODEL_TYPING = typing.Union[ str, None ]

# DETA ATTRIBUTES
PROJECT_KEY = config('PROJECT_KEY', cast=Secret, default='')
PROJECT_ID = config('PROJECT_ID', cast=str, default='')

# TRUSTED HOSTS
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings, default='127.0.0.1, localhost, *.deta.dev')

# SESSION MIDDLEWARE
SESSION_SECRET = config('SESSION_SECRET', cast=str, default='aff18a4d787e9c3668849091701574405451d29666af786cfb71908f51e3c9f1c517f7d3')
SESSION_COOKIE=config('SESSION_COOKIE', cast=str, default='session')
MAX_COOKIE_AGE=config('MAX_COOKIE_AGE', cast=int, default=604800)
SAME_SITE=config('SAME_SITE', cast=str, default='lax')
HTTPS_ONLY=config('HTTPS_ONLY', cast=bool, default=False)

# CORSMiddleware
ALLOW_ORIGINS=config('ALLOW_ORIGINS', cast=list, default=['*'])
ALLOW_HEADERS=config('ALLOW_HEADERS', cast=list, default=['*'])
ALLOW_METHODS=config('ALLOW_METHODS', cast=list, default=['*'])
ALLOW_CREDENTIALS=config('ALLOW_CREDENTIALS', cast=bool, default=True)
ALLOW_ORIGIN_REGEX=config('ALLOW_ORIGIN_REGEX', cast=str, default='htttps://*.deta.dev')
EXPOSE_HEADERS=config('EXPOSE_HEADERS', cast=list, default=['X-Author-Name', 'X-Author-Email'])
MAX_CORS_AGE=config('MAX_CORS_AGE', cast=int, default=600)



oauth = OAuth(config)

oauth.register(
    name=OAUTH_SERVICE,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=OAUTH_CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

