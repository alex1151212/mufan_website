from fastapi import (
    APIRouter ,
    Depends, 
    status ,
    HTTPException,
    Request,
    Cookie
)
from typing import Optional
#Database
from sqlalchemy.orm import Session
from database import get_db
from schemas import *
from crud import *

#Security
from fastapi.security import OAuth2PasswordRequestForm
from oauth import get_current_user


#Image Upload
from fastapi import File ,UploadFile
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image

app = APIRouter(
    
)




@app.post("/register",tags=["User"])
async def user_register(user:CreateUser,db:Session=Depends(get_db)):

    return await register(db,user)

@app.post("/upload_ProfileImg",tags=["User"])
async def create_upload_file(file:UploadFile=File(...),user=Depends(get_current_user),db:Session=Depends(get_db)):

    FILEPATH = './static/images/'
    filename = file.filename

    extension = filename.split(".")[1]

    if extension not in ["png","jpg"]:
        return {"status":"error","detail":"File extension not allowed"}

    token_name = secrets.token_hex(10) + "." + extension
    generated_name = FILEPATH+ token_name
    file_content = await file.read()

    with open(generated_name,"wb") as file :
        file.write(file_content)

    #PILLOW
    img = Image.open(generated_name)
    img = img.resize(size=(200,200))
    img.save(generated_name)


    file.close()

    db_user = db.query(models.User).filter(models.User.username == user["user"]).first()
    
    db_user.profile_img = token_name
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    file_url = "localhost:8000" + generated_name[1:]
    return {"status":"ok","filename":file_url}

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
    res =response.delete_cookie(key="jwt")
    
    return 204

@app.get("/user/me",tags=["User"])
async def userMe(user = Depends(get_current_user)):
        
    return user

@app.post("/userRoles/add",tags=["User"])
async def add_user_roles(username:User_addRoles,roles:List[str],db:Session=Depends(get_db)):

    return await addUserRoles(db,username,roles)

@app.get("/refresh",tags=["User"])
async def refresh_token(jwt:Optional[str]=Cookie(None), db:Session=Depends(get_db)):
    
    return await refreshToken(jw,db)


@app.post("/role" , tags=["Role"])
async def create_role(role:CreateRole,db:Session = Depends(get_db)):
    
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


@app.get('/follow/')
async def user_follow(userid:Optional[str]=None, db:Session=Depends(get_db),user=Depends(get_current_user)):
    
    followedUser = db.query(models.User).filter(models.User.id==userid).first()
    currentUser = db.query(models.User).filter(models.User.username==user['user']).first()
    followedUser.follower.append(currentUser)
    db.commit()
    return followedUser.follower

@app.get('/follower_all/{userid}')
async def get_userfollower_all(userid:str,db=Depends(get_db)):

    user = db.query(models.User).filter(models.User.id==userid).first()

    if not user:
        raise HTTPException(404,detail=f"User with id {userid} is not found")

    return user.follower
