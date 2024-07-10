from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.models import Base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Aniruddhan11121@localhost:5432/Current"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Drop all tables
#Base.metadata.drop_all(bind=engine)

# Create all tables

