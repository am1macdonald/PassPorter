from email_validator import validate_email, EmailNotValidError
from fastapi import Request
from pydantic import EmailStr, SecretStr, ValidationError

from models.Password import Password
from models.PasswordResetToken import PasswordResetToken
from models.User import DBUser, User


class PasswordResetResolver:
    def __init__(self, request: Request, templates):
        self.request = request
        self.templates = templates

    def resolve_request(self, email: EmailStr):
        try:
            email_info = validate_email(email, check_deliverability=False)
            email = email_info.normalized
        except EmailNotValidError as e:
            return self.templates.TemplateResponse(request=self.request,
                                                   name='forms/forgot-password.jinja2',
                                                   context={"to_extend": 'empty.jinja2', "invalid_email": 1,
                                                            "error_message": str(e),
                                                            "email": email})

        user: DBUser = User(email).get_user()
        if not user:
            return self.templates.TemplateResponse(request=self.request,
                                                   name='forms/forgot-password.jinja2',
                                                   context={"to_extend": 'empty.jinja2', "invalid_email": 1,
                                                            "error_message": "A user with this email does not exist",
                                                            "email": email})
        token = PasswordResetToken(user=user)
        if token.exists():
            token.invalidate()
        new_token = PasswordResetToken(user=user)
        new_token.add()
        if not new_token.exists():
            return self.templates.TemplateResponse(request=self.request,
                                                   name='forms/forgot-password.jinja2',
                                                   context={"to_extend": 'empty.jinja2', "failed": 1,
                                                            "error_message": "failed",
                                                            "email": email})

        # TODO: send request to emailer to with reset link
        print('link')

        return self.templates.TemplateResponse(request=self.request, name="views/success.jinja2",
                                               context={"message": f"A link has been sent to your email inbox."})

    def resolve_get_reset(self, token_str: SecretStr):
        valid = False
        token = PasswordResetToken(token_str=token_str)
        if token and token.exists():
            valid = True
        if not valid:
            raise ValueError('not a valid token')
        return self.templates.TemplateResponse(request=self.request, name="forms/reset-password.jinja2",
                                               context={"to_extend": 'index.jinja2',
                                                        "uuid": token_str.get_secret_value()})

    def resolve_reset_action(self, token_str: SecretStr, password: SecretStr, confirm: SecretStr):
        token = PasswordResetToken(token_str=token_str)
        if not token:
            raise ValueError('not a valid token')

        if password != confirm:
            return self.templates.TemplateResponse(
                request=self.request,
                name="forms/reset-password.jinja2",
                context={"to_extend": 'empty.jinja2', "error": 1,
                         "error_message": "Passwords do not match",
                         "invalid_password": 1, "uuid": token_str.get_secret_value()})
        try:
            Password(password=password)
        except ValidationError as e:
            message = e.errors()[0].get('msg').split(',')[1].strip()
            return self.templates.TemplateResponse(
                request=self.request,
                name="forms/reset-password.jinja2",
                context={"to_extend": 'empty.jinja2', "error": 1,
                         "error_message": message,
                         "invalid_password": 1, "uuid": token_str.get_secret_value()})
        user = User(user_id=token.token.user_id)
        if not user.get_user():
            raise ValueError('user does not exist')
        if not user.update_password(password):
            raise ValueError('unable to update')
        token.invalidate()
        return self.templates.TemplateResponse(request=self.request, name="views/success.jinja2",
                                               context={"message": "Your password has been updated", "link_back": 1})
