import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

if os.getenv("TESTING") == "1":
    DATABASE_URL = "sqlite:///./test.db"
else:
    DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()