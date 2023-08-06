import asyncio

import typesystem as ts
from essencia_app.managers import sync_connect


def profile_select_generator(table, request, query={}):
    db = sync_connect(table)
    data = [item for item in next(db.fetch(query))]
    gen = (f'<option value="{instance.get("key")}" class=" bg-light">{instance.get("fullname")}</option>"' for instance in data)
    text = '<div class="container w-50 p-1">'
    text += f'<form action={str(request.url)} method="get" class="p-1 bg-success form-control">'
    text += '<label for="patient_key" class="p-1 bg-success form-control">Selecionar Paciente</label>'
    text += '<select id="patient_key" class="p-1 form-control">'
    try:
        while True:
            text += next(gen)
    except:
        text += '</select>'
        text += '<input type="submit" name="Enviar" class="p-1"/>'
        text += '</fom>'
    finally:
        yield text

