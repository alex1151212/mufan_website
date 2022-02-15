from sqlalchemy import Column,String,Integer,DateTime,func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    username = Column(String(16),unique=True,nullable=False,comment='使用者名稱')
    password = Column(String(50),unique=False,nullable=False,comment='密碼')
    email = Column(String(100),nullable=False,comment="電子信箱")
    phone = Column(String(10),nullable=True,comment="電話")

    created_at = Column(DateTime,server_default=func.now(),comment="創建時間")
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now() ,comment="更新時間")