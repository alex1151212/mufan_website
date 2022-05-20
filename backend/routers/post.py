from pyexpat import model
from turtle import title
from fastapi import (
    APIRouter ,
    Depends,
    Query,
    status ,
    HTTPException,
    Request,
    Cookie,
    Form
)
from typing import Optional
#Database
from sqlalchemy.orm import Session
from database import get_db
from schemas import *
from crud import *
#User
from oauth import get_current_user

#Image Upload
from fastapi import File ,UploadFile
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image

app = APIRouter(
    tags=['Post']
)

@app.post('/post')
async def CreatePost(title=Form(...),post_img:Optional[UploadFile]=None,user = Depends(get_current_user),db:Session=Depends(get_db)):
    
    new_post = models.Post(
        title=title,
        creator_id = db.query(models.User).filter(models.User.username==user['user']).first().id
    ) 


    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    

    FILEPATH = './static/images/'
    filename = post_img.filename

    extension = filename.split(".")[1]

    if extension not in ["png","jpg"]:
        return {"status":"error","detail":"File extension not allowed"}

    token_name = secrets.token_hex(10) + "." + extension
    generated_name = FILEPATH+ token_name
    file_content = await post_img.read()

    with open(generated_name,"wb") as file :
        file.write(file_content)

    #PILLOW
    img = Image.open(generated_name)
    img = img.resize(size=(200,200))
    img.save(generated_name)

    post_img.close()
    
    getPost_id = db.query(models.Post).filter(models.Post.title==title).first()

    new_img = models.Image(
        name = token_name,
        path = "localhost:8000" + generated_name[1:],
        post_id = getPost_id.id
    )

    db.add(new_img)
    db.commit()
    db.refresh(new_img)


    return "Post Success"
# @app.post('/postImg')
# async def postImg(form = Form(...)):

#     # file:UploadFile=File(...)
#     return form

@app.get('/post')
async def testGet(user_id,db:Session=Depends(get_db)):
    
    user =db.query(models.User).filter(models.User.id==user_id).first()
    return user.posts

@app.put('/post')
async def postUpdate(post_id,title=Form(...),post_img:Optional[UploadFile]=None,user = Depends(get_current_user),db:Session=Depends(get_db)):

    if not post_id:
        raise HTTPException(400)

    updated_post = db.query(models.Post).filter(models.Post.id==post_id).first()

    if user['user_id'] != updated_post.creator_id :
        raise HTTPException(401)
    
    updated_post.title = title
    db.add(updated_post)
    db.commit()
    db.refresh(updated_post)

    
    
    # {"type":str(type(title)) }
    return 1

@app.delete('/post')
async def postDelete(post_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):

    post = db.query(models.Post).filter(models.Post.id==post_id)

    if not post.one_or_none() :
        raise HTTPException(400)
    
    if post.one_or_none().creator_id != user["user_id"]:
        raise HTTPException(401)

    post.delete(synchronize_session=False)
    db.commit()

    return "Post delete Success" 

    

@app.post('/comment/{post_id}')
async def createComment(content:Comment,post_id:str,db:Session=Depends(get_db),user=Depends(get_current_user)):

    new_comment = models.Comment(
        **content.dict(),
        creator_id=user["user_id"],
        post_id=post_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return f"Comment for post id {post_id} create success "

@app.get("/comment/{post_id}")
async def getComment_by_postid(post_id:int,db:Session=Depends(get_db)):
    
    comments = db.query(models.Post).filter(models.Post.id==post_id).first().comments

    return comments

@app.put('/comment/{comment_id}')
async def editComment(content:Comment,comment_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    
    editedComment = db.query(models.Comment).filter(models.Comment.id==comment_id).first()

    if not editedComment:
        raise HTTPException(400)

    if editedComment.creator_id != user['user_id']:
        raise HTTPException(401)

    editedComment.content = content.content
    db.add(editedComment)
    db.commit()
    db.refresh(editedComment)

    return "Update Success"

@app.delete('/comment/{comment_id}')
async def deleteComment(comment_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):

    deleteComment = db.query(models.Comment).filter(models.Comment.id==comment_id)

    if not deleteComment.first():
        raise HTTPException(400)

    if deleteComment.first().creator_id != user['user_id']:
        raise HTTPException(401)

    deleteComment.delete(synchronize_session=False)
    db.commit()

    return "Delete Success"