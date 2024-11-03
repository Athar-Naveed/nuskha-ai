import os
from fastapi import FastAPI,HTTPException,status
from typing import Annotated


app:FastAPI = FastAPI()



@app.get("/")
def index():
    return {"message": "Welcome to the Nuskha AI!"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app",reload=True)