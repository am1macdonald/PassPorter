import smtplib
import ssl
from email.mime.text import MIMEText


class MailController:
    def __init__(self, port=None, server=None, email=None, password=None):
        self._port = port
        self._server = server
        self._email = email
        self._password = password
        self.context = ssl.create_default_context()

    def send_mail(self, msg, recipients):
        with smtplib.SMTP_SSL(self._server, self._port, context=self.context) as server:
            server.login(self._email, self._password)
            server.sendmail(self._email, recipients, msg.as_string())

    def compose_message(self, message, subject, recipients: [str]):
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["To"] = ", ".join(recipients)
        msg["From"] = self._email
        return msg
