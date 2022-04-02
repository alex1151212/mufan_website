from fastapi import APIRouter , Depends, status ,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import User,Role,User_addRoles
from crud import *
from fastapi.security import OAuth2PasswordRequestForm
from oauth import get_current_user

router = APIRouter(
    tags=['Users']
)



@router.post("/register",tags=["User"])
def user_register(user:User,db:Session=Depends(get_db)):

    return register(db,user)
    

@router.get("/user/get",tags=["User"])
async def get_user_all(db:Session=Depends(get_db)):

    # user = db.query(models.User).all()
    return await getUser_all(db) 
    # return user
@router.get("/userRoles/get/{username}",tags=["User"])
async def get_user_roles(username:str,db:Session=Depends(get_db),):
   
    return await getUserRoles(db,username)

@router.post("/login",tags=["User"])
async def user_login(user_input= Depends(OAuth2PasswordRequestForm),db:Session = Depends(get_db)):
    
    return await loginUser(db,user_input)

@router.get("/user/me",tags=["User"])
async def userMe(user = Depends(get_current_user)):
        
    return await user

@router.post("/userRoles/add",tags=["User"])
async def add_user_roles(username:User_addRoles,roles:List[str],db:Session=Depends(get_db)):

    return  await addUserRoles(db,username,roles)
    