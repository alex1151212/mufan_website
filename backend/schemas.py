
from ast import Str
import email
from pyexpat import model
from typing import List, Optional

from pydantic import BaseModel,EmailStr

class User(BaseModel):
    username:str
    password:str
    roles:List[int]=None
class CreateUser(BaseModel):
    username:str
    password:str

class Role(BaseModel):
    name:str
    users:List[int]=None
class CreateRole(BaseModel):
    name:str

# class Role_users(BaseModel):
#     users:List[int]
class User_addRoles(BaseModel):
    name:str

# class User_updateImage(User):
#     pass

class Post(BaseModel):
    title:str
    images:List[str]

class Comment(BaseModel):
    content :str

    