from email_validator import validate_email, EmailNotValidError
from fastapi import Request
from pydantic import EmailStr, ValidationError
from pydantic import SecretStr

from controllers.MailController import MailController
from models.EmailVerification import EmailVerification
from models.Password import Password
from models.User import User


class SignupResolver:
    def __init__(self, request: Request, templates, conn=None, mailer: MailController = None):
        self.request = request
        self.templates = templates
        self._conn = conn
        self._mailer = mailer

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

        user = User(email=email, conn=self._conn)
        if user.exists():
            return self.templates.TemplateResponse(
                request=self.request,
                name='forms/sign-up.jinja2',
                context={"to_extend": 'empty.jinja2', "error": 1,
                         "error_message": "User with this email already exists",
                         "invalid_email": 1, "email": email})

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

        user_data = user.add(email, password)
        if not user_data:
            raise ValueError("Can't create user")

        verify = EmailVerification(user_id=user_data[0], conn=self._conn)
        if verify.exists():
            raise ValueError("User verification exists!")

        verify.add(user_id=user_data[0])

        if not verify.exists():
            raise ValueError("Can't verify email")

        link = verify.get_link()
        if link is None:
            raise ValueError("Error generating confirmation link")

        message = f"""
        PassPorter
        
        Here is your verification link:
        {link}
        """
        composed = self._mailer.compose_message(message=message, recipients=[email], subject='Email Verification')
        self._mailer.send_mail(msg=composed, recipients=[email])

        return self.templates.TemplateResponse(request=self.request, name="views/success.jinja2",
                                               context={"message": "A confirmation email has been sent to your inbox."})
