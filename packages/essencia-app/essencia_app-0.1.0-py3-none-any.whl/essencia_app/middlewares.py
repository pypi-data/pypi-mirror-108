import json
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
# PROJECT IMPORTS
from essencia_app import settings
from essencia_app import managers

async def read_path_and_set_context(request: Request):
    try:
        patient_key = request.path_params['patient_key']
        if patient_key:
            async with managers.DbGet('ProfileData', patient_key) as data:
                assert data['model'] == 'Patient'
                settings.cvar_patient.set(data)
    except:
        pass
    try:
        professional_key = request.path_params['professional_key']
        if professional_key:
            async with managers.DbGet('ProfileData', professional_key) as data:
                assert data['model'] == ('Doctor' or 'Therapist' or 'Nurse' or 'Physiotherapist')
                settings.cvar_patient.set(data)
    except:
        pass


class ContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        print(response.headers)
        return response



class MidMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # see above scope dictionary as reference
        assert scope['type'] == 'http'
        request = Request(scope=scope, receive=receive)
        request.state.user = request.session['auth_user']
        if hasattr(request.app.state, 'patient'):
                request.state.patient = request.app.state.patient
        return await self.app(scope, receive, send)


middlewares = [
    Middleware(ContextMiddleware),
    Middleware(SessionMiddleware,
               secret_key=str(settings.SESSION_SECRET),
               session_cookie=settings.SESSION_COOKIE),
    Middleware(MidMiddleware),
    Middleware(CORSMiddleware,
               allow_origins=settings.ALLOW_ORIGINS,
               allow_headers=settings.ALLOW_HEADERS,
               allow_methods=settings.ALLOW_METHODS,
               allow_origin_regex=settings.ALLOW_ORIGIN_REGEX,
               allow_credentials=settings.ALLOW_CREDENTIALS,
               expose_headers=settings.EXPOSE_HEADERS),
    Middleware(TrustedHostMiddleware,
               allowed_hosts=settings.ALLOWED_HOSTS),
    Middleware(ContextMiddleware),

]