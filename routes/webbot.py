from fastapi import APIRouter,Depends,Form,File,UploadFile,status
from typing import Annotated,Optional
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from auth.utils import decoding_jwt_token 
from bots.mobile_bot import medical_grocery_chat
from db.func import storing_chat,retrieving_chats

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app:APIRouter = APIRouter()


async def get_current_user(token:Annotated[dict, Depends(oauth2_scheme)]):
    decoded_data = decoding_jwt_token(token)
    return decoded_data

@app.get("/v1/get_chat")
async def get_chat(
    token: Annotated[dict, Depends(get_current_user)],
    db: Session = Depends(get_db)
    ):
    try:
        chats = retrieving_chats(token['user_id'],db=db)
        return {"message": chats, "status": status.HTTP_200_OK}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": f"Error! {e}", "status": status.HTTP_500_INTERNAL_SERVER_ERROR}

@app.post("/v1/extracting_items")
async def extracting_items(
    token: Annotated[dict, Depends(get_current_user)],
    prompt: Optional[str] = Form(None),
    media_image: Optional[UploadFile] = File(None),
    db:Session = Depends(get_db)
):
    try:
        
        if prompt or media_image:
            resp = await medical_grocery_chat(prompt)
            
            chat = {
                "prompt": prompt,
                "media_image": media_image,
                "resp":str(resp),
                "user_id":token["user_id"]
                }
            store = storing_chat(chat,db=db)
            
            return {"message": resp, "status": status.HTTP_200_OK}
        else:
            return {"message": "Prompt and Media image both can't be empty", "status": status.HTTP_400_BAD_REQUEST}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": f"Error! {e}", "status": status.HTTP_500_INTERNAL_SERVER_ERROR}

