
import email
from typing import Optional

from pydantic import BaseModel,EmailStr

class User(BaseModel):
    username:str
    password:str

class User_register(User):
    email:EmailStr
    phone:str