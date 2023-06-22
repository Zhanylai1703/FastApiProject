from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://api:helloworld@localhost:5432/fastapi"
# SQLALCHEMY_DATABASE_URL = 'postgresql://:%(DB_PASS)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
