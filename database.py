# import necessary libraries
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# database url to the postgre sql database  
DATABASE_URL = "postgresql://postgres:AnTIquE$$5@localhost:5432/chat_app"

# create_engine creates connection between PostgreSQL and SQLAlchemy
engine = create_engine(DATABASE_URL)

# create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class to define a ORM model
Base = declarative_base()

# to get new database session in each API call
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
