import bcrypt
from email_validator import validate_email, EmailNotValidError
from fastapi import Request
from pydantic import EmailStr

from models.PasswordReset import PasswordReset
from models.User import UserLogin, DBUser


class PasswordResetResolver:
    def __init__(self, request: Request, templates):
        self.request = request
        self.templates = templates

    def resolve(self, email: EmailStr):
        try:
            email_info = validate_email(email, check_deliverability=False)
            email = email_info.normalized
        except EmailNotValidError as e:
            return self.templates.TemplateResponse(request=self.request,
                                                   name='forms/forgot-password.jinja2',
                                                   context={"to_extend": 'empty.jinja2', "invalid_email": 1,
                                                            "error_message": str(e),
                                                            "email": email})

        user: DBUser = UserLogin(email).get_user()
        if not user:
            return self.templates.TemplateResponse(request=self.request,
                                                   name='forms/forgot-password.jinja2',
                                                   context={"to_extend": 'empty.jinja2', "invalid_email": 1,
                                                            "error_message": "user with this email does not exist",
                                                            "email": email})
        if not PasswordReset().add(email):
            return self.templates.TemplateResponse(request=self.request,
                                                   name='forms/forgot-password.jinja2',
                                                   context={"to_extend": 'empty.jinja2', "failed": 1,
                                                            "error_message": "failed",
                                                            "email": email})

        return self.templates.TemplateResponse(request=self.request, name="views/success.jinja2",
                                               context={"message": f"A link has been sent to your email inbox."})
