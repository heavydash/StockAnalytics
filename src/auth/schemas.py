from pydantic import BaseModel, ValidationError, validator


class RegistrationIn(BaseModel):
    email: str
    username: str
    hashed_password: str

    @validator('hashed_password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) <= 8:
            raise ValidationError()
        return value

class LoginIn(BaseModel):
    email: str
    hashed_password: str

class LoginOut(BaseModel):
    token: str
