import os
from fastapi import HTTPException,status
from sqlalchemy import Engine,create_engine,String
from sqlalchemy.orm import Mapped,mapped_column,DeclarativeBase
from dotenv import load_dotenv
from media_receive import MediaRequest


class Base(DeclarativeBase):
    pass
class Users(Base):
    __tablename__ = "users"
    user_id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    user_email:Mapped[str] = mapped_column(String(30)) 
    user_pass:Mapped[str] = mapped_column(String(30)) 


load_dotenv()

try:
    connection_url:str = os.getenv("DB_CONNECTION_URL")
    engine:Engine = create_engine(connection_url)
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(e)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=e)