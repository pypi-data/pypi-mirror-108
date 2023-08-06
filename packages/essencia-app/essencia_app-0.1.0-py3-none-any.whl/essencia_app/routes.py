from starlette.routing import Route, Mount

from essencia_app.endpoints import json
from essencia_app.endpoints import html

routes = [
    Route('/', html.Home, name='home', methods=['GET']),
    Route('/json/patients/all', json.PatientsList, name='json-patients-all', methods=['GET']),
    Route('/json/doctors/all', json.DoctorsList, name='json-doctors-all', methods=[ 'GET' ]),
    Route('/patients/all', html.PatientsList, name='html-patients-all', methods=[ 'GET' ]),
    Route('/doctors/all', html.DoctorsList, name='html-doctors-all', methods=[ 'GET' ]),
    Route('/patients/search', html.PatientSearch, name='html-patients-search', methods=[ 'GET', 'POST' ]),
    Route('/patients/create', html.PatientCreate, name='html-patients-create', methods=[ 'GET', 'POST' ]),
    Route('/patients/{patient_key}', html.PatientDetail, name='html-patients-detail', methods=[ 'GET' ]),
    Route('/patients/{patient_key}/update', html.PatientDetail, name='html-patients-update', methods=[ 'GET','POST' ]),
    Route('/patients/{patient_key}/delete', html.PatientDelete, name='html-patients-delete', methods=[ 'GET','POST' ]),
]