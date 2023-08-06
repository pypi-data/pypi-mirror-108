from essencia_app.settings import (TEMPLATES, FORMS)

class TemplateEngine:
    FORMS = FORMS.Form
    TEMPLATES = TEMPLATES

    def __init__(self, request, **kwargs):
        self.request = request
        self.template = kwargs.get('template', '/general.html')
        self.navbar = kwargs.get('navbar', '')
        self.main = kwargs.get('main', '')
        self.side = kwargs.get('side', '')
        self.status = kwargs.get('status', 200)


    def data(self):
        return {k: v for (k, v) in self.__dict__.items() if not k in ['template']}

    def __call__(self, *args, **kwargs):
        return self.TEMPLATES.TemplateResponse(self.template, self.data())

    def render(self):
        return self.TEMPLATES.TemplateResponse(self.template, self.data())


async def render(request, **kwargs):
    return TemplateEngine(request, **kwargs).render()


if __name__ == '__main__':
    render = TemplateEngine('', navbar='teste', main='main', side='side')
    print(render.data())
    print(render.render())