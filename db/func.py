from fastapi import HTTPException,status,Depends
from sqlalchemy.orm import Session
from type.chat_type import ChatType
from models.auth_model import UserChats

def storing_chat(
        chat:ChatType,
        db:Session):
    try:
        chat_data = UserChats(user_prompt=chat['prompt'],chat_image=chat['media_image'],bot_response=chat['resp'],users=chat["user_id"])
        db.add(chat_data)
        db.commit()
        db.refresh(chat_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Error storing chat: {e}"}
        )