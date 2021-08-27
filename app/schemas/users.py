from pydantic import BaseModel, EmailStr, validator
import re


def validate_password(password: str):
    regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$"
    pattern = re.compile(regex)
    if not pattern.match(password):
        raise ValueError('Password is invalid.')
    return password


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class CreateUser(UserBase):
    password: str

    _validate = validator('password', allow_reuse=True)(validate_password)


class ChangeUserPassword(BaseModel):
    password: str

    _validate = validator('password', allow_reuse=True)(validate_password)


class LoginUser(BaseModel):
    access_token: str
    refresh_token: str
