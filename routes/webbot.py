import uuid
from fastapi import APIRouter,Depends,Form,File,UploadFile,status,BackgroundTasks
from typing import Annotated,Optional
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from auth.utils import decoding_jwt_token 
from db.func import storing_chat,retrieving_chats

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app:APIRouter = APIRouter()

async def get_current_user(token:Annotated[dict, Depends(oauth2_scheme)]):
    decoded_data = decoding_jwt_token(token)
    return decoded_data

@app.get("/get_chat",tags=["Get Chats"])
async def get_chat(
    token: Annotated[dict, Depends(get_current_user)],
    db: Session = Depends(get_db)
    ):

    """
    Extracting Chats -- v1 (current version)
    This function retrieves chats from the database.
    :param token: User's JWT token.
    :return: Chats.
    """
    try:
        chats = retrieving_chats(token['user_id'],db=db)
        return {"messages": chats, "status": status.HTTP_200_OK}
    except Exception as e:
        print(f"Error: {e}")
        return {"messages": f"Error! {e}", "status": status.HTTP_500_INTERNAL_SERVER_ERROR}

@app.post("/extracting_items",tags=["Extracting Items"])
async def extracting_items(
    token: Annotated[dict, Depends(get_current_user)],
    background_tasks:BackgroundTasks,
    prompt: Optional[str] = Form(None),
    media_image: Optional[UploadFile] = File(None),
    db:Session = Depends(get_db)
):
    from pathlib import Path
    from bots.mobile_bot import medical_grocery_chat
    """
    Extracting Items -- v1 (current version)
    This function extracts items from a given prompt and media image.
    :param token: User's JWT token.
    :param prompt: Prompt to extract items from.
    :param media_image: Media image to extract items from.
    :return: Extracted items.
    """
    # -----------------------
    # Media upload dir starts
    # -----------------------
    UPLOAD_DIR = Path("/tmp/images")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    # -----------------------
    # Media upload dir ends
    # -----------------------
    try:
        
        image_path = None
        if media_image:
            file_ext = media_image.filename.split(".")[1]
            image_path =UPLOAD_DIR / f"{uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')}.{file_ext}"
            with open(image_path,"wb") as buffer:
                buffer.write(await media_image.read())
        # import pdb; pdb.set_trace()
        if prompt or media_image:
            resp = await medical_grocery_chat(prompt,image_path)
            
            chat = {
                "prompt": prompt,
                "media_image": "",
                "resp":str(resp),
                "user_id":token["user_id"]
                }
            background_tasks.add_task(storing_chat,chat,db=db)
            
            return {"message": resp, "status": status.HTTP_200_OK}
        else:
            return {"message": "Prompt and Media image both can't be empty", "status": status.HTTP_400_BAD_REQUEST}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": f"Error! {e}", "status": status.HTTP_500_INTERNAL_SERVER_ERROR}

