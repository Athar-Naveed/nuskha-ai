from fastapi import FastAPI,Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from auth import auth
# from routes import chatbot,webbot
from database import init_db


async def lifespan(app:FastAPI):
    init_db()
    yield
    

app:FastAPI = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.include_router(auth.app,prefix="/auth")
# app.include_router(webbot.app,prefix="/webbot/v1")

# from chat_socket.socket_config import socket_app
# app.mount("/socket.io", socket_app)

# app.mount('/images', StaticFiles(directory="images"), name="images")

@app.get("/")
async def index():
    return {"message": "Welcome to the Nuskha AI!"}

@app.post("/token")
async def token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    print(f"form data username: {form_data.username}")
    print(f"form data password: {form_data.password}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app",reload=True)