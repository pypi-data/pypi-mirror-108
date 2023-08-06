import datetime
import typesystem as ts

from essencia_app import abstract as abs

definitions = ts.SchemaDefinitions()

### SEARCH MODELS

class PersonKeyFullname(ts.Schema):
    key = ts.String()
    fullname = ts.String()

class PatientSearch(ts.Schema):
    name = ts.String(min_length=3)


class Profile(ts.Schema, abs.Base, definitions=definitions):
    fullname = ts.String()
    class Gender(abs.StrEnum):
        Male = 'Masculino'
        Female = 'Feminino'
    gender = ts.Choice(choices=Gender)
    birthdate = ts.Date()

    @property
    def age(self):
        bdate = self.birthdate if isinstance(self.birthdate, datetime.date) else datetime.date.fromisoformat(self.birthdate)
        return ((datetime.date.today() - bdate).days / 365).__round__(1)


    @property
    def age_str(self):
        bdate = self.birthdate if isinstance(self.birthdate, datetime.date) else datetime.date.fromisoformat(self.birthdate)
        age = ((datetime.date.today() - bdate).days / 365).__round__(1)
        if age <= 1:
            return ' '.join([str(age), 'ano'])
        return ' '.join([str(age), 'anos'])

class Patient(Profile):
    pass

class Provider(Profile):
    profession = ts.String(title='Profissão')
    licence = ts.String(title='Registro Profissional')
    graduation = ts.Integer(title='Ano de Graduação')


class Subjective(ts.Schema, abs.Base, definitions=definitions):
    main_complaints = ts.Text(title='Queixa Principal', allow_blank=True)
    clinical_picture = ts.Text(title='Apresentação Clínica', allow_blank=True)

class Pharmacotherapy(ts.Schema, abs.Base, definitions=definitions):
    medication = ts.String()
    posology = ts.String(allow_blank=True)
    pro = ts.String(allow_blank=True)
    con = ts.String(allow_blank=True)


class Treatment(ts.Schema, abs.Base, definitions=definitions):
    pharmacotherapy = ts.Array(items=[ts.Reference(to='Pharmacotherapy')], allow_null=True)
    psychotherapy = ts.Text(allow_blank=True)


class Objective(ts.Schema, abs.Base, definitions=definitions):
    weight = ts.Float(minimum=0, maximum=250, description='Kg', allow_null=True)
    hr = ts.Integer(minimum=0, maximum=300, description='batimentos por minuto', allow_null=True)
    bp = ts.String(title='pressão sanguínea', description='mmHg', allow_blank=True)
    mental = ts.Text(title='Exame Mental', allow_blank=True)
    physical = ts.Text(title='Exame Físico', allow_blank=True)


class Notes(ts.Schema, abs.Base, definitions=definitions):
    subjective = ts.Reference(to='Subjective', definitions=definitions)
    objective = ts.Reference(to='Objective', definitions=definitions, allow_null=True)


class Visit(ts.Schema, abs.Base, definitions=definitions):
    patient = ts.Reference(to='Profile', definitions=definitions)
    provider = ts.Reference(to='Profile', definitions=definitions)
    notes = ts.Reference(to='Notes', definitions=definitions)

