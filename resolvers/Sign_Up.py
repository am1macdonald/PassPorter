from email_validator import validate_email, EmailNotValidError
from fastapi import Request
from pydantic import EmailStr, field_validator, ValidationError
from pydantic import SecretStr

from models.SignupPassword import SignupPassword
from models.User import NewUser


class SignupResolver:
    def __init__(self, request: Request, templates):
        self.request = request
        self.templates = templates

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
                         "error_message": "passwords do not match",
                         "invalid_password": 1, "email": email})
        try:
            SignupPassword(password=password)
        except ValidationError as e:
            message = e.errors()[0].get('msg').split(',')[1].strip()
            return self.templates.TemplateResponse(
                request=self.request,
                name='forms/sign-up.jinja2',
                context={"to_extend": 'empty.jinja2', "error": 1,
                         "error_message": message,
                         "invalid_password": 1, "email": email})
        NewUser(email, password).add()
        return self.templates.TemplateResponse(request=self.request, name="views/signup_success.jinja2")
