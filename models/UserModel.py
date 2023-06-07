from typing import List

from fastapi import Form, UploadFile
from pydantic import BaseModel, Field, EmailStr
from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()


class UserModel(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    photo: str = Field(...)
    token: str

    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        schema_extra = {
            "user": {
                "name": "string",
                "email": "string",
                "password": "string",
                "photo": "string",
            }
        }


@decoratorUtil.form_body
class UserCreateModel(BaseModel):
    name: str = Field(max_length=50, min_length=3)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "user": {
                "name": "Fulano de tal",
                "email": "fulano@gmail.com",
                "password": "SeNha123!",
            }
        }


class UserLoginModel(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "user": {
                "email": "fulano@gmail.com",
                "password": "SeNha123!",
            }
        }


@decoratorUtil.form_body
class UserUpdateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    photo: UploadFile = Field(...)

    class Config:
        schema_extra = {
            "user": {
                "name": "Fulano de tal",
                "email": "fulano@gmail.com",
                "password": "SeNha123!",
            }
        }