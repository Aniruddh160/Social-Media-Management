from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, text, LargeBinary
from sqlalchemy.orm import relationship
from app.database import Base, engine
from app.schemas import *
import base64

class User(Base):
    __tablename__ = "Users"
    U_ID = Column(Integer, primary_key=True)
    Email = Column(String, unique=True, index=True, nullable=False)
    Password = Column(String, nullable=False)
    U_Is_Active = Column(Boolean, default=True)
    U_Created_AT = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    followers_count = Column(Integer, nullable=False, default=0)
    
    messages = relationship("TextsTone", back_populates="owner")
    followers = relationship("Follow", foreign_keys="Follow.followed_id", back_populates="followed")
    following = relationship("Follow", foreign_keys="Follow.follower_id", back_populates="follower")

class TextsTone(Base):
    __tablename__ = "Texts_Tone"
    T_ID = Column(Integer, primary_key=True, nullable=False)
    T_Title = Column(String, nullable=False)
    T_Content = Column(String, nullable=False)
    T_Published = Column(Boolean, default=True, nullable=False)
    T_Created_AT = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    Owner_id = Column(Integer, ForeignKey("Users.U_ID"), nullable=False)
    owner = relationship("User", back_populates="messages")
    images = relationship("Posts_image", back_populates="post", cascade="all, delete-orphan")

# class Posts_image(Base):
#     __tablename__ = "Posts_image"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     post_id = Column(Integer, ForeignKey('Texts_Tone.T_ID', ondelete='CASCADE'), nullable=False)
#     image_url = Column(String, nullable=False)
#     post = relationship("TextsTone", back_populates="images")

    
class Posts_image(Base):
    __tablename__ = "Posts_image"
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('Texts_Tone.T_ID', ondelete='CASCADE'), nullable=False)
    image_url = Column(String, nullable=False, default="default_image_url")
    post = relationship("TextsTone", back_populates="images")
    
    
    

    
class Vote(Base):
    __tablename__ = "votes"
    
    post_id = Column(Integer, ForeignKey("Texts_Tone.T_ID"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.U_ID"), primary_key=True, nullable=False)
     
    
class Follow(Base):
    __tablename__ = "follows"
    follower_id = Column(Integer, ForeignKey("Users.U_ID"), primary_key=True, nullable=False)
    followed_id = Column(Integer, ForeignKey("Users.U_ID"), primary_key=True, nullable=False)
    
    follower = relationship("User", foreign_keys=[follower_id])
    followed = relationship("User", foreign_keys=[followed_id])
    
    
Base.metadata.create_all(bind=engine)
    
    
    
    