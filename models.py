
from itertools import product
from sqlalchemy import Column, ForeignKey,Integer , String,Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

# from app.database import Base
# from app.database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Posts(Base): 
    __tablename__ = "posts"
    id = Column(Integer , primary_key=True,  nullable= False )
    title = Column(String , nullable= False)
    content = Column(String , nullable= False)
    published = Column(Boolean , server_default='TRUE', nullable=False )
    created_at = Column(TIMESTAMP(timezone= True) , nullable=False , server_default= text('now()'))
    owner_id = Column(Integer , ForeignKey("users.id" , ondelete= "CASCADE") , nullable=False)
    # relation will the User data also with the help of foreignkey
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key=True ,nullable=False)
    email = Column(String , nullable=False , unique=True)
    password = Column(String , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False , server_default=text("now()"))
    # phone_number = Column(String , nullable=False)
    

# likes table
# 
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer , ForeignKey("users.id" , ondelete="CASCADE") , primary_key=True)
    post_id = Column(Integer , ForeignKey("posts.id" , ondelete="CASCADE") , primary_key=True)

class Store(Base):
    __tablename__ = "store"
    product_name = Column(String , nullable=False)
    Product_id = Column(String, nullable=False , primary_key=True)
    product_size = Column(String , nullable=False)