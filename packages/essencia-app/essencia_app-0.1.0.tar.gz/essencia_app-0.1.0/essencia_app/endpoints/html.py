import contextvars

from starlette.endpoints import HTTPEndpoint, HTTPException
from starlette.requests import Request
from markupsafe import Markup
import re

from essencia_app import managers as manager
from essencia_app import utils
from essencia_app import models
from essencia_app.utils import elements as el
from essencia_app.utils.render import render, TemplateEngine
from essencia_app import settings
from essencia_app.endpoints.handlers import base as base_hand


class Home(HTTPEndpoint):
    async def get(self, request: Request):
        name = el.Title('Essência Psiquiatria',1)
        return await render(request, navbar=name())


class PatientsList(HTTPEndpoint):
    async def get(self, request: Request):
        async with manager.DbAll('Patient') as data:
            objects = (models.PersonKeyFullname(item) for item  in data)
            links = []
            try:
                while True:
                    i = next(objects)
                    links.append(el.Link(
                        text=getattr(i, 'fullname'),
                        href=f"{request.url_for('html-patients-detail', patient_key=getattr(i, 'key'))}")
                    )
            except StopIteration:
                pass
            objects_list = el.UnOlList(items=[i for i in links]).klass('overflow-auto')
            title = el.Title(text='Lista de Pacientes',level=2)
            content = el.Div(text=objects_list()).klass('bg-light p-2')
            main = el.Div(text=title + content).klass('bg-light p-5 overflow-auto')
            return await render(request, main=Markup(main))


class PatientDetail(HTTPEndpoint):
    async def get(self, request: Request):
        await base_hand.read_path_and_set_context(request)
        links = [
            el.Link('Deletar', href=request.url_for('html-patients-delete', patient_key=request.path_params['patient_key'])),
            el.Link('Editar',
                    href=request.url_for('html-patients-update', patient_key=request.path_params[ 'patient_key' ])),
        ]
        async with manager.DbGet('Patient', key=request.path_params['patient_key']) as data:
            settings.cvar_patient.set(data)
            request.app.state.patient = settings.cvar_patient.get()
            print('request.state.patient set to:', request.app.state.patient)
            request.app.state.user = request.session['auth_user']
            patient = models.Profile(request.state.ctx.patient.get())
            print(patient)
            detail = '''
            <muted>PACIENTE</muted><br>
            <h3>{fullname}</h3>
            <hr>
            Idade: {age}<br>
            Nascimento: {birthdate}<br>
            Gênero: {gender}<br>
            '''.format(
                fullname=patient.fullname,
                age=patient.age_str,
                birthdate=patient.birthdate,
                gender=patient.gender,
            )
            text = el.Div(Markup(Markup(detail) + el.Div('\n\n'.join([l.render for l in links])).render))
            return await render(
                request,
                side=Markup(el.Div(text=Markup(text)).klass('p-3 border border-dark')),
            )

class DoctorsList(HTTPEndpoint):
    async def get(self, request: Request):
        async with manager.DbSearch('Doctor') as data:
            return await render(request, main=data)

class PatientCreate(HTTPEndpoint):
    async def get(self, request: Request):
        blank_form = TemplateEngine.FORMS(models.Patient)
        title = el.Title('Adicionar Paciente',4)
        form = el.Form(blank_form.render_fields(), action=request.url.path, method='post').klass('form-control')
        main = Markup(title() + form())
        return await render(request, main=main)

    async def post(self, request: Request):
        data = await request.form()
        title = el.Title('Adicionar Paciente',4)
        patient, error = models.Patient.validate_or_error(data)
        if error:
            blank_form = TemplateEngine.FORMS(models.Patient, values=data, errors=error)
            form = el.Form(blank_form.render_fields(), action=request.url.path, method='post').klass(
                'form-control')
            main = Markup(title() + form())
            return await render(request, main=main)
        patient.setup_metadata()
        async with manager.DbCheckCode('ProfileBase', code=patient.code) as exist:
            if exist == True:
                raise HTTPException(detail='Este paciente já existe', status_code=409)
            async with manager.DbPut('ProfileBase', patient.full_json()) as result:
                request.state.patient_create_result = result
                print(f'{self.__class__.__name__}:', result)
        text = '''
        Paciente criado com sucesso!
        {patient}
        '''.format(
            patient=patient.full_json()
        )
        return await render(request, main=Markup(text))


class PatientSearch(HTTPEndpoint):
    async def get(self, request: Request):
        blank_form = TemplateEngine.FORMS(models.PatientSearch)
        form = el.Form(blank_form.render_fields(), action=request.url.path, method='post', input_value='buscar paciente').render
        text = el.Div(form).klass('p-3 bg-light')
        return await render(request, main=Markup(text))

    async def post(self, request: Request):
        fdata = await request.form()
        name = fdata.get('name')
        print('query name', name)
        cname = re.match('\w+', name) or ''
        async with manager.DbSearchByName('ProfileBase', cname.group()) as data:
            if data:
                result = [models.PersonKeyFullname(item) for item in data]
                print('result from patient search', result)
                title = el.Title('Resultado de Pacientes', 4)()
                links = [el.Link(text=patient.fullname, href=request.url_for('html-patients-detail', patient_key=patient.key)).klass('p-2')() for patient in result]
                ulist = el.UnOlList(items=links, ol=True).klass('p-2')()
                main = el.Div(text=title + ulist).klass('p-2')()
                return await render(request, main=Markup(main))
            title = el.Title('Nenhum paciente encontrado', 4)()
            link = el.Link('Adicionar Paciente', href=request.url_for('html-patients-create')).klass('btn btn-primary p-2')()
            main = Markup(title + link)
            return await render(request, main=Markup(main))


class PatientDelete(HTTPEndpoint):
    async def get(self, request: Request):
        content = [
            'Você deseja realmente deletar este objeto?'
            'Esta ação não poderá ser desfeita.'
        ]
        patient = models.Profile(request.app.state.patient)
        print(patient)
        detail = '''
        <muted>PACIENTE</muted><br>
        <h3>{fullname}</h3>
        <hr>
        Idade: {age}<br>
        Nascimento: {birthdate}<br>
        Gênero: {gender}<br>
        '''.format(
            fullname=patient.fullname,
            age=patient.age_str,
            birthdate=patient.birthdate,
            gender=patient.gender,
        )
        text = el.Div(
            Markup('\n'.join(content) + detail)
        ).klass('p-3').render
        return await render(request, main=text)