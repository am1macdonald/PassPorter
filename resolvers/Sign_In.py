import bcrypt
from email_validator import validate_email, EmailNotValidError
from fastapi import Request
from pydantic import EmailStr
from pydantic import SecretStr

from models.User import User, DBUser


class SigninResolver:
    def __init__(self, request: Request, templates):
        self.request = request
        self.templates = templates

    @staticmethod
    def _check_password(password, password_hash):
        return bcrypt.checkpw(password.get_secret_value().encode(), password_hash.get_secret_value().encode())

    def resolve(self, email: EmailStr, password: SecretStr):
        try:
            email_info = validate_email(email, check_deliverability=False)
            email = email_info.normalized
        except EmailNotValidError as e:
            return self.templates.TemplateResponse(request=self.request,
                                                   name='forms/sign-in.jinja2',
                                                   context={"to_extend": 'empty.jinja2', "invalid_email": 1,
                                                            "error_message": str(e),
                                                            "email": email})

        user: DBUser = User(email).get_user()
        if not user:
            return self.templates.TemplateResponse(request=self.request,
                                                   name='forms/sign-in.jinja2',
                                                   context={"to_extend": 'empty.jinja2', "invalid_email": 1,
                                                            "error_message": "A user with this email does not exist",
                                                            "email": email})
        if not self._check_password(password, user.password_hash):
            return self.templates.TemplateResponse(request=self.request,
                                                   name='forms/sign-in.jinja2',
                                                   context={"to_extend": 'empty.jinja2', "invalid_password": 1,
                                                            "error_message": "Wrong password",
                                                            "email": email})

        return self.templates.TemplateResponse(request=self.request, name="views/success.jinja2",
                                               context={"message": f"Welcome {user.username}!"})
