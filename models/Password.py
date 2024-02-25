from pydantic import BaseModel, SecretStr, field_validator, ValidationError


class Password(BaseModel):
    password: SecretStr

    @field_validator('password')
    @classmethod
    def validate_password(cls, password: SecretStr) -> SecretStr:
        unwrapped_password = password.get_secret_value()
        if len(unwrapped_password) < 8:
            raise ValueError('Password should be at least 8 characters long')
        if not any(char.isdigit() for char in unwrapped_password):
            raise ValueError('Password should contain at least one digit')
        if not any(char.isalpha() for char in unwrapped_password):
            raise ValueError('Password should contain at least one letter')
        if not any(not char.isalnum() for char in unwrapped_password):
            raise ValueError('Password should contain at least one symbol')
        return password
