
from ast import Str
from distutils.util import strtobool
import email
from pyexpat import model
from typing import List, Optional

from pydantic import BaseModel, EmailStr
import models


class User(BaseModel):
    username: str
    password: str
    roles: List[int] = None

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    username: str
    password: str


class Role(BaseModel):
    name: str
    users: List[int] = None


class CreateRole(BaseModel):
    name: str


class User_addRoles(BaseModel):
    name: str


class Ticketing(BaseModel):
    title: str
    price: int
    description: str
    tickets: int
    isSoldout: Optional[bool] = False


class CreateTicketing(Ticketing):
    id: int

# ResponseModel for Profile


class Post(BaseModel):
    title: str
    images: List[str]

    class Config:
        orm_mode = True


class Comment(BaseModel):
    content: str

    class Config:
        orm_mode = True


class Posts(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class Roles(BaseModel):
    # id:int
    name: str

    class Config:
        orm_mode = True


class Followers(BaseModel):
    # id:int
    username: str

    class Config:
        orm_mode = True


class UserAll(BaseModel):

    username: str
    roles: List[Roles] = []
    posts: List[Posts] = []
    comments: List[Comment] = []
    follower: List[Followers] = []

    class Config:
        orm_mode = True
