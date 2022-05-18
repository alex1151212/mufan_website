from fastapi import FastAPI
from sqlalchemy import Column,String,Integer,DateTime,func,ForeignKey,Table, null
from sqlalchemy.orm import relationship
from database import Base


role_manager = Table(
    "Role_Manager",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), nullable=False, primary_key=True),
    Column("role_id", Integer, ForeignKey("role.id"), nullable=False, primary_key=True)
)

followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id',Integer,ForeignKey('user.id')),
    Column('followed_id',Integer,ForeignKey('user.id')),
)

posts_category = Table(
    "Posts_category",
    Base.metadata,
    Column('post_id',Integer,ForeignKey('post.id')),
    Column('category_id',Integer,ForeignKey('category.id'))
)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(16),unique=True,nullable=False,comment='使用者名稱')
    password = Column(String(50),unique=False,nullable=False,comment='密碼')
    # roles = Column(String(10),nullable=True,comment="roles",default="User")
    email = Column(String(100),nullable=True,comment="電子信箱")
    phone = Column(String(10),nullable=True,comment="電話")
    profile_img = Column(String(100),nullable=True)

    roles = relationship('Role',secondary=role_manager,back_populates='users')
    posts = relationship('Post',back_populates="creator")
    comments = relationship('Comment',back_populates="creator")

    follower = relationship(
        'User',
        secondary = followers,
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id),
        backref = ('faned_users'),
    )

    created_at = Column(DateTime,server_default=func.now(),comment="創建時間")
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now() ,comment="更新時間")


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer,nullable=False, primary_key=True)
    name = Column(String(10),nullable=False,comment="Role_Name")

    users = relationship('User',secondary=role_manager,back_populates='roles')


class Post(Base):
    __tablename__ = "post" 

    id = Column(Integer,nullable = False,primary_key=True)
    title = Column(String(50),nullable=False,comment="Post_title")
    creator_id = Column(Integer,ForeignKey("user.id"))
    images = relationship('Image')
    

    creator = relationship('User',back_populates='posts')
    categories = relationship('Category',secondary=posts_category,back_populates="posts")
    comments = relationship('Comment',back_populates="at")

    created_at = Column(DateTime,server_default = func.now(),comment="建立時間")
    updated_at = Column(DateTime,server_default = func.now(),comment="最後編輯時間")

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer,nullable = False,primary_key=True)
    name = Column(String(20),nullable=False)

    posts = relationship('Post',secondary=posts_category,back_populates="categories")

class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer,nullable = False,primary_key=True)
    content = Column(String(100),nullable=False)
    creator_id = Column(Integer,ForeignKey("user.id"))
    post_id = Column(Integer,ForeignKey("post.id"))

    at = relationship('Post',back_populates='comments')
    creator = relationship('User',back_populates='comments')

    created_at = Column(DateTime,server_default = func.now(),comment="建立時間")
    updated_at = Column(DateTime,server_default = func.now(),comment="最後編輯時間")

class Image(Base):
    __tablename__ = "image"

    id = Column(Integer,nullable = False,primary_key=True)
    name = Column(String(100),nullable=False)
    path = Column(String(100),nullable=False)
    post_id = Column(Integer,ForeignKey('post.id'))


    created_at = Column(DateTime,server_default = func.now(),comment="建立時間")
