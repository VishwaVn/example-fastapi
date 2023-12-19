from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from .config import settings
import pymysql
import time

username = settings.database_username
password = settings.database_password
hostname = settings.database_hostname
port = settings.database_hostname
database_name = settings.database_name

# Encode special characters in the password
# encoded_password = quote(password, safe="")
encoded_password = quote(settings.database_password, safe="")
# Construct the SQLAlchemy database URL
# SQLALCHEMY_DATABASE_URL = (
#     f"mysql://{username}:{encoded_password}@{hostname}:{port}/{database_name}"
# )
SQLALCHEMY_DATABASE_URL = f"mysql://{settings.database_username}:{encoded_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# create an engine with Sqlalchemy_URL
# then create a SessionLocal = sessionmaker()
# Base = declarative_base()

# dependency


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = pymysql.connect(
#             host="localhost",
#             user="root",
#             password=settings.database_password,
#             db="fastapi",
#         )
#         cursor = conn.cursor()
#         print(f"Database was successfully created")
#         break
#     except Exception as error:
#         print(f"Connecting to database failed")
#         print(f"Error : {error}")
#         time.sleep(2)
