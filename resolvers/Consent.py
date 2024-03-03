from fastapi import Request
from fastapi.responses import RedirectResponse

from models.Client import Client


class ConsentResolver:
    def __init__(self, request: Request, templates):
        self.request = request
        self.templates = templates
        self.query = request.query_params

    def resolve_get(self):
        client = Client(self.request.query_params.get("client_id")).get()
        if not client:
            return {'error': True, 'message': 'client does not exist'}
        if self.query.get("redirect_uri") not in client.redirect:
            return {'error': True, 'message': 'invalid redirect'}
        if not self.request.cookies.get('token'):
            return RedirectResponse(f'/sign-in?{self.request.query_params}')
        print(self.request.url.query)
        scope = self.query.get('scope')
        return self.templates.TemplateResponse(request=self.request, name='forms/consent.jinja2',
                                               context={"to_extend": 'index.jinja2', "client_name": client.client_name,
                                                        "scope": scope,
                                                        "items": ["Email Address", "Username"],
                                                        "query_params": f"{self.request.query_params}"
                                                        })
