from fastapi import Request
from fastapi.responses import RedirectResponse

from models.EmailVerification import EmailVerification


class VerifyEmailTokenResolver:
    def __init__(self, request: Request, conn = None):
        self.request = request
        self._conn = conn

    def resolve(self, email_token: str):
        v_token = EmailVerification(token=email_token, conn=self._conn)
        if not v_token.exists():
            raise ValueError("Token does not exist")
        if not v_token.is_valid() or v_token.is_expired():
            raise ValueError("Token is invalid")
        if not v_token.consume():
            raise ValueError("Error consuming token")
        return RedirectResponse('/sign-in', status_code=308)


