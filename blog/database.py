from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHAMY_DATABASE_URL = 'sqlite:///./blog.db'

# Connection arg only needed for sqlite
engine = create_engine(SQLALCHAMY_DATABASE_URL,connect_args={"check_same_thread": False})

# Each instance of sessionLocal is a DB connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()