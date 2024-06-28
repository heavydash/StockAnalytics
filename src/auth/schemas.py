from pydantic import BaseModel, ValidationError, validator


class RegistrationIn(BaseModel):
    email: str
    username: str
    password: str

    @validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) <= 8:
            raise ValidationError()
        return value

class LoginIn(BaseModel):
    email: str
    password: str

class LoginOut(BaseModel):
    token: str
