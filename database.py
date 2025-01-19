import os
from fastapi import HTTPException,status
from sqlalchemy import Engine,create_engine
from sqlalchemy.orm import Session,sessionmaker
from dotenv import load_dotenv
from models.auth_model import Base
load_dotenv()


connection_url:str = os.getenv("DB_CONNECTION_URL")
engine:Engine = create_engine(connection_url)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=e)
    

# dependency here, its work is to create a new session on each request and close it when the request is fulfilled.
def get_db():
    db:Session = session_local()
    try:
        yield db
    finally:
        db.close()