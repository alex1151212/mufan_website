from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError,jwt
from JWTtoken import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        user = payload.get("user")
        roles = payload.get("roles")
        return {"user":user,"role":roles}
    except:
        raise HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )
