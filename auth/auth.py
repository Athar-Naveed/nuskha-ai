from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from models.auth_model import Users
from database import get_db

app:APIRouter = APIRouter()


@app.post("/login")
async def login(email:str, password:str):
    try:
        return {'email':email, 'password':password,'status':status.HTTP_202_ACCEPTED}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please try again later!") 
        


@app.post("/register")
async def register(first_name:str, last_name:str, email:str, password:str,db:Session=Depends(get_db)):
    try:
        user = Users(first_name=first_name,last_name=last_name,user_email=email,user_pass=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {'firstName':first_name,'lastName':last_name,'email':email, 'password':password,'status':status.HTTP_201_CREATED}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please try again later!") 