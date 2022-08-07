from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    Request,
    Cookie,
    Response
)
from typing import Optional
from sqlalchemy import true
# Database
from sqlalchemy.orm import Session
from database import get_db
from schemas import *
from crud import *

# Security
from fastapi.security import OAuth2PasswordRequestForm
from oauth import get_current_user
import JWTtoken


# Image Upload
from fastapi import File, UploadFile
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image

app = APIRouter(

)


@app.post("/signup", tags=["User", "Api"])
async def user_signup(user: CreateUser, db: Session = Depends(get_db)):

    new_user = models.User(
        username=user.username,
        password=Hash.bcrypt(user.password),
    )

    user_exist = db.query(models.User).filter(
        models.User.username == user.username).first()
    if user_exist:
        raise HTTPException(409)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/verify", tags=["User", "Api"])
async def user_login(response: Response, user_input=Depends(OAuth2PasswordRequestForm), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.username == user_input.username).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail=f'沒有此用戶'
        )
    if not Hash.verify(user.password, user_input.password):
        raise HTTPException(
            status_code=401,
            detail=f"使用者帳號或密碼錯誤!"
        )
    roles = []
    for role in user.roles:
        roles.append(role.name)
    access_token = JWTtoken.create_access_token(
        data={
            "user": user.username,
            "roles": roles,
            'user_id': user.id
        }
    )
    refresh_token = JWTtoken.create_access_token(
        data={
            "user": user.username,
        }
    )
    response.set_cookie(key="jwt", value=refresh_token, httponly=True)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.username,
        "roles": roles,
    }


@app.get('/siguout', tags=['User', "Api"], deprecated=true)
async def user_logout(response: Response, req: Request):
    res = response.delete_cookie(key="jwt")

    return 204


@app.post("/user/profile-img", tags=["User", "Api"])
async def upload_user_profile_img(file: UploadFile = File(...), user=Depends(get_current_user), db: Session = Depends(get_db)):

    FILEPATH = './static/img/profile'
    filename = file.filename

    extension = filename.split(".")[1]

    if extension not in ["png", "jpg"]:
        return {"status": "error", "detail": "File extension not allowed"}

    token_name = secrets.token_hex(10) + "." + extension
    generated_name = FILEPATH + token_name
    file_content = await file.read()

    with open(generated_name, "wb") as file:
        file.write(file_content)

    # PILLOW
    img = Image.open(generated_name)
    img = img.resize(size=(200, 200))
    img.save(generated_name)

    file.close()

    db_user = db.query(models.User).filter(
        models.User.username == user["user"]).first()

    db_user.profile_img = token_name
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    file_url = "localhost:8000" + generated_name[1:]
    return {"status": "ok", "filename": file_url}


@app.get("/dev/user", tags=["User", "Dev-Api"], response_model=List[UserAll])
async def get_all_users(db: Session = Depends(get_db)):

    user = db.query(models.User).all()

    return user

# TODO set get user roles orm_mode = true


@app.get("/user/me", tags=["User", "Dev-Api"])
async def userMe(user=Depends(get_current_user)):

    return user


@app.get("/profile", tags=["User", "Api"], response_model=UserAll)
async def userMe(db: Session = Depends(get_db), user=Depends(get_current_user)):

    profile = db.query(models.User).filter(
        models.User.username == user["user"]).one_or_none()

    return profile


@app.patch("/user/roles/", tags=["User", "Api"])
async def add_user_roles(username: User_addRoles, roles: List[str], db: Session = Depends(get_db)):

    for role in roles:
        R = db.query(models.Role).filter(models.Role.name == role).first()

        if not R:
            raise HTTPException(404, detail=f"Role with name {role} Not Found")

        user_role = db.query(models.User).filter(
            models.User.username == username.name).first()
        user_role.roles.append(R)

    db.commit()

    return "Roles Add Success!"


@app.get('/user/posts')
async def get_user_posts(user_id, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user.posts


@app.get("/refresh", tags=["User", "Dev-Api"])
async def refresh_token(jwt: Optional[str] = Cookie(None), db: Session = Depends(get_db)):

    token = JWTtoken.decode_access_token(jwt)

    user = db.query(models.User).filter(
        models.User.username == token['user']).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail=f'沒有此用戶'
        )
    roles = []
    for role in user.roles:
        roles.append(role.name)
    access_token = JWTtoken.create_access_token(
        data={
            "user": user.username,
            "roles": roles,
            'user_id': user.id
        },
        expire_delta=0.5
    )
    return {
        "accessToken": access_token,
        "token_type": "bearer",
        "user": user.username,
        "roles": roles,
    }


@app.post("/role", tags=["Role", "Dev-Api"])
async def create_role(role: CreateRole, db: Session = Depends(get_db)):

    new_role = models.Role(
        name=role.name
    )

    role_exist = db.query(models.Role).filter(
        models.Role.name == role.name).first()
    if role_exist:
        raise HTTPException(409)

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role


@app.get("/role/{role_name}", tags=["Role", "Dev-Api"])
async def get_role_byname(role_name: str, db: Session = Depends(get_db)):

    role = db.query(models.Role).filter(models.Role.name == role_name).first()

    if not role:
        raise HTTPException(404, detail="Role Not Found")

    return role


@app.get("/role", tags=["Role"])
async def get_role_all(db: Session = Depends(get_db)):

    role = db.query(models.Role).all()

    if not db.query(models.Role).first():
        raise HTTPException(404, detail="Role Not Found")

    return role


@app.get("/dev/role/{name}", tags=["Role", "Dev-Api"])
async def get_role_users(name: str, db: Session = Depends(get_db)):

    role = db.query(models.Role).filter(models.Role.name == name).first()

    if not role:
        raise HTTPException(404, detail="Role Not Found")

    return role


@app.patch("/role/{role_name}", tags=["Role"])
async def update_role_byname(role_name: str, new_role: Role, db: Session = Depends(get_db)):

    role = db.query(models.Role).filter(models.Role.name == role_name)

    if not role.first():
        raise HTTPException(
            404, detail=f"Role with name {role_name} Not Found")

    role.update(new_role)
    db.commit()

    return "Update Role Success!"


@app.delete("/role/{role_name}", tags=["Role"])
async def delete_role_byname(role_name: str, db: Session = Depends(get_db)):

    role = db.query(models.Role).filter(models.Role.name == role_name)

    if not role.first():
        raise HTTPException(
            404, detail=f"Role with name {role_name} Not Found")

    role.delete(synchronize_session=False)
    db.commit()

    return "Delete Role Successfully!"


@app.post('/follow/', tags=["Api", "User"])
async def user_follow(userid: Optional[str] = None, db: Session = Depends(get_db), user=Depends(get_current_user)):

    followedUser = db.query(models.User).filter(
        models.User.id == userid).first()
    currentUser = db.query(models.User).filter(
        models.User.username == user['user']).first()
    followedUser.follower.append(currentUser)
    db.commit()
    return followedUser.follower


@app.delete('/follow', tags=["Api", "User"])
async def user_follow(userid: Optional[str] = None, db: Session = Depends(get_db), user=Depends(get_current_user)):

    unfollowedUser = db.query(models.User).filter(
        models.User.id == userid).first()
    currentUser = db.query(models.User).filter(
        models.User.username == user['user']).first()

    unfollowedUser.follower.remove(currentUser)
    db.commit()
    return unfollowedUser.follower


@app.get('/follower_all/{userid}', tags=["Dev-Api", "User"])
async def get_userfollower_all(userid: str, db=Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == userid).first()

    if not user:
        raise HTTPException(404, detail=f"User with id {userid} is not found")

    return user.follower
