# app/config/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
from dotenv import load_dotenv
from .settings import Settings

load_dotenv()

if os.getenv("APP_ENV") =='test':
    SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:password123@localhost:5432/bank'
else:
    settings = Settings()
    SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    up = False
    while not up:
    
        try:  
            db = SessionLocal() 
            yield db
        except Exception as err:
            print(f"Connection error: {err}")
            up = False
        else:
            up = True
        finally:
            db.close()
    

