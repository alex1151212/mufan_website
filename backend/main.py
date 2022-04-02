from typing import List, Optional
from fastapi import Cookie, FastAPI , Depends ,Response,Request

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

# app.include_router(user.router)
# app.include_router(role.router)

Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return await "Hello World!"


@app.post("/register",tags=["User"])
async def user_register(user:User,db:Session=Depends(get_db)):

    return await register(db,user)
    
@app.get("/users",tags=["User"])
async def get_user_all(db:Session=Depends(get_db)):

    # user = db.query(models.User).all()
    return await getUser_all(db) 
    # return user
@app.get("/userRoles/get/{username}",tags=["User"])
async def get_user_roles(username:str,db:Session=Depends(get_db),):
   
    return await getUserRoles(db,username)

@app.post("/login",tags=["User"])
async def user_login(response:Response,user_input= Depends(OAuth2PasswordRequestForm),db:Session = Depends(get_db)):
    
    return await loginUser(db,user_input,response)

@app.get('/logout',tags=['User'])
async def user_logout(response:Response,req:Request):
    res =response.delete_cookie(key="Authorization")
    
    return 204

@app.get("/user/me",tags=["User"])
async def userMe(user = Depends(get_current_user)):
        
    return user

@app.post("/userRoles/add",tags=["User"])
async def add_user_roles(username:User_addRoles,roles:List[str],db:Session=Depends(get_db)):

    return await addUserRoles(db,username,roles)

@app.get("/refresh")
async def refresh_token(response:Response,Authorization:Optional[str]=Cookie(None), db:Session=Depends(get_db)):
    
    return await refreshToken(response,Authorization,db)
# @app.get('/users',tags=["User"])
# async def get_user_byRole_all(db:Session=Depends(get_db)):
#     pass
# ROLE

@app.post("/role" , tags=["Role"])
async def create_role(role:Role,db:Session = Depends(get_db)):
    
    return await createRole(db,role)


@app.get("/role/{role_name}" ,tags=["Role"])
async def get_role_byname(role_name:str,db:Session = Depends(get_db)):
    
    return await getRole_byName(db,role_name)

@app.get("/role" ,tags=["Role"])
async def get_role_all(db:Session = Depends(get_db)):

    return await getRole_all(db)


@app.get("/roleUsers/get/{name}" ,tags=["Role"])
async def get_role_users(name:str,db:Session = Depends(get_db)):

    return await getRoleUser(db,name)


@app.put("/role/{role_name}" ,tags=["Role"])
async def update_role_byname(role_name:str,new_role:Role,db:Session = Depends(get_db)):
    
    return await updateRoleName_byName(db,role_name,new_role)

@app.delete("/role/{role_name}" ,tags=["Role"])
async def delete_role_byname(role_name:str,db:Session = Depends(get_db)):

    return await deleteRole_byName(db,role_name )