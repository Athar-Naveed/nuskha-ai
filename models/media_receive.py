from fastapi import UploadFile,Form,File
from pydantic import BaseModel
from typing import Annotated,Optional

class MediaRequest(BaseModel):
    prompt: Optional[str] = Form(None)
    media_image: Optional[UploadFile] = File(None)