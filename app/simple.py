from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from app.routers.users import router
from app.routers.post import router1
from app.routers.auth import router2
from app.routers.votes import router3
from app.routers.follow import router4
from .models import *

#Router imported from various Router files(user.py and post.py)
app1 = FastAPI()
app1.include_router(router)
app1.include_router(router1)
app1.include_router(router2)
app1.include_router(router3)
app1.include_router(router4)


# Database configuration
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Aniruddhan11121@localhost/Current"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




    
    
# Database Connection
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password='Aniruddhan11121',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Hello Aniruddh Lets start working on the Project")
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection failed")
        print("error: ", error)
        time.sleep(2)



 




    
