import os

import jwt
from jwt import InvalidTokenError


class AuthController:
    def __init__(self):
        self.jwt_secret = os.environ["JWT_SECRET"]

    def issue_token(self, payload):
        return jwt.encode(payload, self.jwt_secret, algorithm="RS256")

    def decode_token(self, token):
        return jwt.decode(token, self.jwt_secret, algorithms=["RS256"],
                          options={"verify_signature": True, "verify_exp": True})

    def validate_token(self, token):
        try:
            jwt.decode(token, self.jwt_secret, algorithms=["RS256"],
                       options={"verify_signature": True, "verify_exp": True})
            return True
        except InvalidTokenError as e:
            print("Invalid Token: " + e)
            return False
