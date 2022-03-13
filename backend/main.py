from typing import List
from fastapi import FastAPI , Depends

from database import Base,engine,get_db
from sqlalchemy.orm.session import Session

from schemas import User,Role,User_addRoles

from oauth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

import JWTtoken

from crud import *
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return "Hello World!"

#Todo-User register
@app.post("/register",tags=["User"])
def user_register(user:User,db:Session=Depends(get_db)):

    return register(db,user)
    

@app.get("/user/get",tags=["User"])
def get_user_all(db:Session=Depends(get_db),):

    return getUser_all(db) 

@app.get("/userRoles/get/{username}",tags=["User"])
def get_user_roles(username:str,db:Session=Depends(get_db),):
   
    return getUserRoles(db,username)

@app.post("/login",tags=["User"])
def user_login(user_input= Depends(OAuth2PasswordRequestForm),db:Session = Depends(get_db)):
    
    return loginUser(db,user_input)

@app.get("/user/me",tags=["User"])
async def userMe(user = Depends(get_current_user)):
        
    return user

@app.post("/userRoles/add",tags=["User"])
async def add_user_roles(username:User_addRoles,roles:List[str],db:Session=Depends(get_db)):

    return addUserRoles(db,username,roles)
    

@app.post("/role" , tags=["Role"])
async def create_role(role:Role,db:Session = Depends(get_db)):
    
    return createRole(db,role)


@app.get("/role/{role_name}" ,tags=["Role"])
async def get_role_byname(role_name:str,db:Session = Depends(get_db)):
    
    return getRole_byName(db,role_name)

@app.get("/role" ,tags=["Role"])
async def get_role_all(db:Session = Depends(get_db)):

    return getRole_all(db)


@app.get("/roleUsers/get/{name}" ,tags=["Role"])
async def get_role_users(name:str,db:Session = Depends(get_db)):

    return getRoleUser(db,name)


@app.put("/role/{role_name}" ,tags=["Role"])
async def update_role_byname(role_name:str,new_role:Role,db:Session = Depends(get_db)):
    
    return updateRoleName_byName(db,role_name,new_role)

@app.delete("/role/{role_name}" ,tags=["Role"])
async def delete_role_byname(role_name:str,db:Session = Depends(get_db)):

    return deleteRole_byName(db,role_name )