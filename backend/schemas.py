
import email
from typing import List, Optional

from pydantic import BaseModel,EmailStr

class User(BaseModel):
    username:str
    password:str
    roles:List[int]=None

class Role(BaseModel):
    name:str
    users:List[int]=None

# class Role_users(BaseModel):
#     users:List[int]
class User_addRoles(BaseModel):
    name:str

class User_updateImage(User):
    pass