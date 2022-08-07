from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from JWTtoken import *
from database import SessionLocal
import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="verify")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user = payload.get("user")
        roles = payload.get("roles")
        user_id = payload.get('user_id')
        return {"user": user, "role": roles, "user_id": user_id}
    except:
        raise HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

# def get_current_user1(db:Session ,token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("user")
#         roles :str = payload.get("roles")
#         if username is None:
#             raise credentials_exception

#     except JWTError:
#         raise credentials_exception
#     user = db.query(models.User).filter(models.User.username==username).first()
#     if user is None:
#         raise credentials_exception
#     return {"user":user,"role":roles}
