from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url) # pyright: ignore[reportArgumentType]
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind = engine)
Base = declarative_base()

#Create a Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()