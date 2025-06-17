from pydantic import BaseModel
class RegisterType(BaseModel):
    first_name:str
    last_name:str
    email:str
    password:str
class LoginType(BaseModel):
    email:str
    password:str
class RegisterResponseType(BaseModel):
    message:str
    auth_token:str
    status:int
class LoginResponseType(BaseModel):
    message:str
    auth_token:str
    status:int
    