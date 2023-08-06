from starlette.endpoints import HTTPEndpoint, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from essencia_app import managers as manager

class PatientsList(HTTPEndpoint):
    async def get(self, request: Request):
        print(str(request.url))
        async with manager.DbAll('Patient') as data:
            return JSONResponse(data, status_code=200)

class DoctorsList(HTTPEndpoint):
    async def get(self, request: Request):
        async with manager.DbAll('Doctor') as data:
            return JSONResponse(data, status_code=200)

