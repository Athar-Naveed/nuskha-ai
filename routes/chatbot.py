from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from bots.mobile_bot import medical_grocery_chat
from chat_socket.socket_config import sio
from auth.utils import decoding_jwt_token 
from database import get_db
from db.func import storing_chat,retrieving_chats

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@sio.event
async def connect(sid,environ):
    print(f"User {sid} connected")
    await sio.emit("send_msg", "Hello from Server")

@sio.event
async def disconnect(sid, environ):
    print(f"User {sid} disconnected")

async def get_current_user(token:Annotated[dict, Depends(oauth2_scheme)]):
    decoded_data = decoding_jwt_token(token)
    return decoded_data

@sio.on("sendMessage")
async def send_message(
    # token: Annotated[dict, Depends(get_current_user)],
    sid, data):
    # ,db:Session = Depends(get_db)):
    print(f"Message from: {sid}: {data}")
        # we need to think how to store user chat in db
        # chat = {
        #         "prompt": data['text'],
        #         # "media_image": media_image,
        #         "resp":str(resp),
        #         "user_id":token["user_id"]
        #         }
        # store = storing_chat(chat,db=db)
    # this will broadcast the message to all the users
    # await sio.emit("message", data)
    # response = await chatbot.extracting_items(prompt=data)
    # print(f"response: {response}")
    # this will send the message back to the sender only
    async for chat in medical_grocery_chat(data['text']):  
        await sio.emit("message", {"message":chat,"role":"ai"}, to=sid)
