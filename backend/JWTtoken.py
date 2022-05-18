from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException
from jose import JWTError,jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_MINUTES = 5

def create_access_token(data:dict,expire_delta:Optional[timedelta]= None):
    to_encode = data.copy()
    if expire_delta :
        expire = datetime.utcnow() + timedelta(minutes=expire_delta)
    else :
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        user = payload.get("user")
        roles = payload.get("roles")
        return {"user":user,"role":roles}
    except:
        raise HTTPException(
            status_code=401, detail="Invalid Authorization"
        )