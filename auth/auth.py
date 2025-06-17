
from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from models.auth_model import Users
from database import get_db
from auth.utils import encoding_jwt_token,decoding_jwt_token,hash_password,verifying_password
from type.auth_type import *
app:APIRouter = APIRouter()


@app.post("/login",tags=["Auth"],response_model=LoginResponseType)
async def login(
    data:LoginType,
    db: Session = Depends(get_db),
):
    try:
        user = db.query(Users).filter(Users.user_email == data['email']).first()
        if user is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":"User not found!","status":status.HTTP_404_NOT_FOUND})
    
        verified_password = verifying_password(data['password'],user.user_pass)
        if not verified_password:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail={"message":"Invalid Password!","status":status.HTTP_401_UNAUTHORIZED})
        
        token = encoding_jwt_token({"user_id":user.user_id,"user_email":user.user_email,"user_name":f"{user.first_name} {user.last_name}"})
        return {"message":"User Logged In Successfully!","auth_token":token,"status":status.HTTP_200_OK}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message":"Please try again later!"}) 
        


@app.post("/register",tags=["Auth"],response_model=RegisterResponseType)
async def register(
    data:RegisterType,
    db: Session = Depends(get_db),
):
    try:
        # Check if email is already registered
        existing_user = db.query(Users).filter(Users.user_email == data['email']).first()
        if existing_user:
            return HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": "Email already registered!","status":status.HTTP_409_CONFLICT},
            )
        hashed_pass = hash_password(data['password'])
        user = Users(
            first_name=data['first_name'],
            last_name=data['last_name'],
            user_email=data['email'],
            user_pass=hashed_pass,
        )
        db.add(user)
        hashed_token = encoding_jwt_token(data)
        db.commit()
        db.refresh(user)
        return {"message": "User created successfully!","auth_token":hashed_token,"status":status.HTTP_201_CREATED}
    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Please try again later!"},
        )