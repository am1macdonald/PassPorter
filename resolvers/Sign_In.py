import bcrypt
from email_validator import validate_email, EmailNotValidError
from fastapi import Request
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
from pydantic import SecretStr

from models.User import User, DBUser


class SigninResolver:
    def __init__(self, request: Request, templates, conn):
        self.request = request
        self.templates = templates
        self.conn = conn
        self.client = None

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
                                                   context={"to_extend": 'index.jinja2', "invalid_email": 1,
                                                            "error_message": str(e),
                                                            "email": email})
        user = User(conn=self.conn, email=email)
        user_value: DBUser = user.get_user()
        if not user.exists():
            return self.templates.TemplateResponse(request=self.request,
                                                   name='forms/sign-in.jinja2',
                                                   context={"to_extend": 'index.jinja2', "invalid_email": 1,
                                                            "error_message": "A user with this email does not exist",
                                                            "email": email})
        if user_value.attempts > 3:
            return self.templates.TemplateResponse(request=self.request,
                                                   name='forms/sign-in.jinja2',
                                                   context={"to_extend": 'index.jinja2', "invalid_email": 1,
                                                            "error_message": "Account locked: Too many attempts",
                                                            "email": email})

        if not self._check_password(password, user_value.password_hash):
            user.add_attempt()
            return self.templates.TemplateResponse(request=self.request,
                                                   name='forms/sign-in.jinja2',
                                                   context={"to_extend": 'index.jinja2', "invalid_password": 1,
                                                            "error_message": "Wrong password",
                                                            "email": email})

        token = user.get_token()
        user.update_login_time()
        client_id = self.request.query_params.get("client_id")
        if client_id:
            redirect_url = f"/consent?{self.request.query_params}"
            response = RedirectResponse(url=redirect_url, status_code=303)
            response.set_cookie(key="token", value=token)
            return response

        return self.templates.TemplateResponse(request=self.request, name="views/success.jinja2",
                                               context={"to_extend": "index.jinja2",
                                                        "message": f"Welcome {user_value.username}!"})
