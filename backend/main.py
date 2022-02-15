from xml.parsers.expat import model
from fastapi import FastAPI , Depends, Form

from database import Base,engine,get_db
import models 
from sqlalchemy.orm.session import Session

from schemas import User_register
from hash import Hash

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return "Hello World!"

#Todo-User register
@app.post("/user")
def user_register(user:User_register,db:Session=Depends(get_db)):
    
    new_user = models.User(
        username=user.username,
        password=Hash.bcrypt(user.password),
        email = user.email,
        phone = user.phone,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/getuser")
def get_all_user(db:Session=Depends(get_db),):
    user = db.query(models.User).all()
    return user