from contextvars import Context
from starlette.requests import Request
from essencia_app import settings
from essencia_app import managers

async def read_path_and_set_context(request: Request):
    request.state.ctx = Context()
    try:
        patient_key = request.path_params['patient_key']
        if patient_key:
            async with managers.DbGet('ProfileData', patient_key) as data:
                assert data['model'] == 'Patient'
                request.state.ctx.__setattr__('patient', data)
    except:
        pass
    try:
        professional_key = request.path_params['professional_key']
        if professional_key:
            async with managers.DbGet('ProfileData', professional_key) as data:
                assert data['model'] == ('Doctor' or 'Therapist' or 'Nurse' or 'Physiotherapist')
                request.state.ctx.__setattr__(data['model'].lower(), data)


    except:
        pass

    print({k:v for k,v in request.state.ctx.items()})

