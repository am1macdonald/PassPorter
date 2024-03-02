import os
import uuid
from datetime import datetime, timedelta

import jwt
from jwt import InvalidTokenError


class AuthController:
    def __init__(self):
        self.jwt_secret = os.environ["JWT_SECRET"]

    def issue_token(self, payload: dict):
        data = {"iat": datetime.now(),
                "exp": datetime.now() + timedelta(days=7),
                "iss": "passporter",
                "jti": str(uuid.uuid4()),
                "context": payload}
        return jwt.encode(data, self.jwt_secret, algorithm="HS256")

    def decode_token(self, token):
        return jwt.decode(token, self.jwt_secret, algorithms=["HS256"],
                          options={"verify_signature": True, "verify_exp": True})

    def validate_token(self, token):
        try:
            jwt.decode(token, self.jwt_secret, algorithms=["HS256"],
                       options={"verify_signature": True, "verify_exp": True})
            return True
        except InvalidTokenError as e:
            print("Invalid Token: " + e)
            return False
