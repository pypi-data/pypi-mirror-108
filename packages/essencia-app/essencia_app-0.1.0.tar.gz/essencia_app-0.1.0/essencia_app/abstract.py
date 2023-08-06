import datetime
from abc import ABC
from enum import Enum

class StrEnum(str, Enum):
    def __str__(self):
        return self.value


class Base(ABC):

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        for k,v in kwargs.items():
            setattr(self, k, v)


    def setup_metadata(self, **kwargs):
        if hasattr(self, 'birthdate'):
            if isinstance(self.birthdate, str):
                self.birthdate = datetime.date.fromisoformat(self.birthdate)
        if not hasattr(self, 'model'):
            setattr(self, 'model', kwargs.get('model') or self.__class__.__name__)
        if not hasattr(self, 'table'):
            setattr(self, 'table', kwargs.get('table') or self.__class__.__name__ + 'Base')
        if not hasattr(self, 'created'):
            setattr(self, 'created', datetime.datetime.now())
        if kwargs.get('request'):
            setattr(self, 'owner', kwargs.get('request').session['auth_user'])
        if not hasattr(self, 'code'):
            setattr(self, 'code', self.find_code())

    def find_code(self):
        if self.__class__.__name__ in ['Person', 'Profile', 'Patient', 'Doctor', 'Therapist', 'Employee', 'Assistant']:
            return f'{self.birthdate.isoformat().replace("-","")}{self.fullname.split()[0][0]}{self.fullname.split()[-1][0]}_{self.__class__.__name__}'
        return f'{self.created.isoformat().split()[0].replace("-","").replace(":","")}{self.__class__.__name__}'

    def json(self):
        return {k: str(v) for (k, v) in self.__dict__.items() if v != None and not k in ['model', 'table', 'owner', 'code', 'created']}

    def full_json(self, **kwargs):
        self.setup_metadata(**kwargs)
        x = self.__dict__
        x.update(kwargs)
        return {k: str(v) for (k, v) in x.items() if v != None}


