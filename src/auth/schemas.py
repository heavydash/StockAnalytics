from typing import Optional, List

from pydantic import BaseModel, ValidationError, validator



class RegistrationIn(BaseModel):
    email: str
    username: str
    password: str

    @validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) <= 8:
            raise ValidationError()
        return value


