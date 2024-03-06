from email_validator import validate_email, EmailNotValidError
from fastapi import Request
from pydantic import EmailStr, ValidationError
from pydantic import SecretStr

from models.Password import Password
from models.User import User


class SignupResolver:
    def __init__(self, request: Request, templates, conn = None):
        self.request = request
        self.templates = templates
        self._conn = conn

    def resolve(self, email: EmailStr, password: SecretStr, confirm: SecretStr):
        try:
            email_info = validate_email(email, check_deliverability=False)
            email = email_info.normalized
        except EmailNotValidError as e:
            return self.templates.TemplateResponse(request=self.request,
                                                   name='forms/sign-up.jinja2',
                                                   context={"to_extend": 'empty.jinja2', "invalid_email": 1,
                                                            "error_message": str(e),
                                                            "email": email})
        if password != confirm:
            return self.templates.TemplateResponse(
                request=self.request,
                name='forms/sign-up.jinja2',
                context={"to_extend": 'empty.jinja2', "error": 1,
                         "error_message": "Passwords do not match",
                         "invalid_password": 1, "email": email})
        try:
            Password(password=password)
        except ValidationError as e:
            message = e.errors()[0].get('msg').split(',')[1].strip()
            return self.templates.TemplateResponse(
                request=self.request,
                name='forms/sign-up.jinja2',
                context={"to_extend": 'empty.jinja2', "error": 1,
                         "error_message": message,
                         "invalid_password": 1, "email": email})
        User(email, password).add()
        return self.templates.TemplateResponse(request=self.request, name="views/success.jinja2",
                                               context={"message": "A confirmation email has been sent to your inbox."})
