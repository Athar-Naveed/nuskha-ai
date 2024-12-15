import os

from fastapi import APIRouter,Depends,status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import google.generativeai as genai
from sqlalchemy.orm import Session,sessionmaker
from database import get_db
from models.media_receive import MediaRequest


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = APIRouter()


genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel("gemini-1.5-pro")

async def get_current_user(token:Annotated[dict,Depends(oauth2_scheme)]):
    pass

@app.post("/v1/extracting_items")
async def extracting_items(
    # token:Annotated[dict, Depends(get_current_user)],
    user_request: MediaRequest
    ):
    print(f"user_request: {user_request}")
    if user_request.prompt or user_request.media_image:
        return {"message": user_request.prompt, "status":status.HTTP_200_OK}
    else:
        return {"message":"Prompt and Media image both can't be empty","status":status.HTTP_400_BAD_REQUEST}
