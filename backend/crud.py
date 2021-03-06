from typing import List
from fastapi import Depends , HTTPException, Response
from sqlalchemy.orm import Session
from database import get_db
from schemas import *
from hash import Hash
import JWTtoken
import models

# Users CRUD


async def register(db:Session,user:CreateUser):

    new_user = models.User(
        username=user.username,
        password=Hash.bcrypt(user.password),
    )

    user_exist = db.query(models.User).filter(models.User.username==user.username).first()
    if user_exist:
       raise HTTPException(409) 
       
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

async def getUser_all(db:Session):

    user = db.query(models.User).all()

    return user

async def getUserRoles(db:Session,username:str):
    
    user = db.query(models.User).filter(models.User.username==username).first()
    return user.roles

async def loginUser(db:Session, userInput,response):

    user = db.query(models.User).filter(models.User.username==userInput.username).first()
    if not user : 
        raise HTTPException(
            status_code = 400 , 
            detail = f'沒有此用戶'
            )
    if not Hash.verify(user.password,userInput.password):
        raise HTTPException(
            status_code= 401,
            detail = f"使用者帳號或密碼錯誤!"
        )
    roles = []
    for role in user.roles:
        roles.append(role.name)
    access_token = JWTtoken.create_access_token(
        data={
            "user":user.username,
            "roles":roles,
            'user_id':user.id
        }
    )
    refresh_token = JWTtoken.create_access_token(
        data={
            "user":user.username,
        }
    )
    response.set_cookie(key="jwt",value=refresh_token,httponly=True)
    return {
        "access_token":access_token ,
        "token_type":"bearer",
        "user":user.username,
        "roles":roles,
        }


async def refreshToken(authToken,db:Session):
    token = JWTtoken.decode_access_token(authToken)

    user = db.query(models.User).filter(models.User.username==token['user']).first()
    if not user : 
        raise HTTPException(
            status_code = 400 , 
            detail = f'沒有此用戶'
            )
    roles = []
    for role in user.roles:
        roles.append(role.name)
    access_token = JWTtoken.create_access_token(
        data={
            "user":user.username,
            "roles":roles,
            'user_id':user.id
        },
        expire_delta=0.5
    )
    return {
        "accessToken":access_token ,
        "token_type":"bearer",
        "user":user.username,
        "roles":roles,
        } 

async def addUserRoles(db:Session,username:User_addRoles,roles:List[str]):
    
    for role in roles:
        R = db.query(models.Role).filter(models.Role.name==role).first()
        
        if not R :
            raise HTTPException(404,detail=f"Role with name {role} Not Found")

        user_role = db.query(models.User).filter(models.User.username==username.name).first()
        user_role.roles.append(R)

    db.commit()
    return "Roles Add Success!"

async def createRole(db:Session,role:CreateRole):

    new_role = models.Role(
        name=role.name
    )

    role_exist = db.query(models.Role).filter(models.Role.name == role.name).first()
    if role_exist:
       raise HTTPException(409) 
    
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    return new_role

async def getRole_byName(db:Session,role_name:str):

    role = db.query(models.Role).filter(models.Role.name==role_name).first()
    
    if not role:
        raise HTTPException(404,detail="Role Not Found")

    return role

async def getRole_all(db:Session):

    role = db.query(models.Role).all()
    
    if not db.query(models.Role).first() :
        raise HTTPException(404,detail="Role Not Found")

    return role

async def getRoleUser(db:Session,name:str):

    role = db.query(models.Role).filter(models.Role.name==name).first()
    
    if not db.query(models.Role).first() :
        raise HTTPException(404,detail="Role Not Found")

    return role.users

async def updateRoleName_byName(db:Session,role_name:str,new_role:Role):
   
    role = db.query(models.Role).filter(models.Role.name==role_name)
    
    if not role.first() :
        raise HTTPException(404,detail=f"Role with name {role_name} Not Found")

    role.update(new_role)
    db.commit()
    
    return "Update Role Success!"

async def deleteRole_byName(db:Session,role_name:str, ):

    role = db.query(models.Role).filter(models.Role.name==role_name)

    if not role.first():
        raise HTTPException(404,detail=f"Role with name {role_name} Not Found")

    role.delete(synchronize_session=False)
    db.commit()
    
    return "Delete Role Successfully!"