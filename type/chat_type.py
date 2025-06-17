from pydantic import BaseModel
class ChatType(BaseModel):
    prompt: str
    media_image: str
    bot_response: str

