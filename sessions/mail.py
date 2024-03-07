import os
from controllers.MailController import MailController

mail = MailController(port=os.environ["SMTP_PORT"], password=os.environ["GMAIL_APP_PASSWORD"],
                      email=os.environ["EMAIL_ADDRESS"], server=os.environ["SMTP_SERVER"])

