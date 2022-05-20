from fastapi import (
    APIRouter,
    Depends,
    Form,
    status,
    HTTPException,
    Request,
    Cookie
)
from typing import Optional
import redis
# Database
from sqlalchemy.orm import Session
from database import get_db
from schemas import *
from crud import *

# Security
from fastapi.security import OAuth2PasswordRequestForm
from oauth import get_current_user

#Redis
import aioredis

app = APIRouter(

)

@app.on_event("startup")
async def startup_event():
    # aioredis.Redis(host="127.0.0.1",port=6379,db=3,encoding="utf-8")
    redis = aioredis.from_url("redis://localhost")
    # await redis.set("my-key", "value")
    # value = await redis.get("my-key")
    # print(value)
    print(f"redis成功--->>{redis}")

@app.post('/ticketing')
async def CreateTicketing(ticketing: Ticketing, db: Session = Depends(get_db)):

    new_ticketing = models.Ticketing(
        **ticketing.dict()
    )

    
    db.add(new_ticketing)
    db.commit()
    db.refresh(new_ticketing)

    t = db.query(models.Ticketing).filter(models.Ticketing.title==ticketing.title).first()
    redis = aioredis.from_url("redis://localhost")

    await redis.hmset(f'TicketingId_{t.id}',{"isSoldout":str(t.isSoldout),"ticket":t.tickets})

    return ticketing

@app.get('/ticketing')
async def GetTicketing_ALL(db:Session = Depends(get_db)):
    
    ticketing = db.query(models.Ticketing).all()

    return ticketing

@app.get('/ticket/buy/{ticketing_id}')
async def buyticket(db:Session=Depends(get_db),user=Depends(get_current_user)):
    
    pass
    
@app.get('/123')
async def test():

    redis = aioredis.from_url("redis://localhost")
    await redis.hmset("Htest",{"a":1,"b":2,"c":3})