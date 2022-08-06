import configparser
from typing import List, Optional
from fastapi import Cookie, FastAPI, Depends, Response, Request
from fastapi.staticfiles import StaticFiles
from database import Base, engine, get_db
from sqlalchemy.orm.session import Session

from schemas import User, Role, User_addRoles

from oauth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from routers import user, post, tickets

from crud import *

from dotenv import dotenv_values
config = dotenv_values('.env')

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*'],
)

app.mount('/static', StaticFiles(directory="static"), name="static")

app.include_router(user.app)
app.include_router(post.app)
app.include_router(tickets.app)


Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return "Hello World!"


@app.get('/config')
def test():
    return config
