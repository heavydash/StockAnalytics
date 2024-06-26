from pydantic import BaseModel, validator
from datetime import time, datetime

class SecurityTradeIn(BaseModel):
    Security_Id: str
    Tradeno: int
    Tradetime: time
    Boardid: str
    Prise: float
    Quantity: int
    Value: float
    Period: str
    Yied: float
    Tradetime_grp: int
    Systime: datetime
    Buysell: str
    Decimals: int
    Tradingsession: str

    @validator('Prise')
    @classmethod
    def validate_prise(cls, v):
        if v <= 0:
            raise ValueError('Prise must be greater than 0')
        return v

    @validator('Quantity')
    @classmethod
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be greater than 0')
        return v

    @validator('Tradetime')
    @classmethod
    def validate_tradetime(cls, v):
        if v >= datetime.now().time():
            raise ValueError('Tradetime must be in the past')
        return v

    class Config:
        orm_mode = True

class SecurityTradeOut(BaseModel):
    Security_Id: str
    Tradeno: int
    Tradetime: time
    Boardid: str
    Prise: float
    Quantity: int
    Value: float
    Period: str
    Yied: float
    Tradetime_grp: int
    Systime: datetime
    Buysell: str
    Decimals: int
    Tradingsession: str

    class Config:
        orm_mode = True

class SecurityIn(BaseModel):
    NAME: str

    @validator('NAME')
    @classmethod
    def validate_name(cls, v):
        if not v or len(v) > 100:
            raise ValueError('NAME must not be empty or exceed 100 characters')
        return v


class SecurityOut(BaseModel):
    NAME: str

    class Config:
        orm_mode = True
