from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserInfo(BaseModel):
    username: str = Field(..., example="username")
    email: EmailStr = Field(..., example="email")


class UserInfoIn(UserInfo):
    password: str = Field(..., example="password")


class UserInfoOut(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str

    class Config:
        orm_mode = True


class TransctionInfoIn(BaseModel):
    customer_name: str = Field(..., example="customer_name")
    gas_price: float = Field(..., example="800.00", )
    gas_quantity: float = Field(..., example="8")
    total_price: float = Field(..., example="8983.00")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = None
