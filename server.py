import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import auth
from routes import chatbot

app:FastAPI = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.app,prefix="/auth")
app.include_router(chatbot.app)


@app.get("/")
def index():
    return {"message": "Welcome to the Nuskha AI!"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app",reload=True)
