from fastapi import APIRouter,HTTPException,status


app:APIRouter = APIRouter()


@app.post("/login")
async def login(email:str, password:str):
    try:
        return {'email':email, 'password':password,'status':status.HTTP_202_ACCEPTED}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please try again later!") 
        


@app.post("/register")
async def register(first_name:str, last_name:str, email:str, password:str):
    try:
        return {'firstName':first_name,'lastName':last_name,'email':email, 'password':password,'status':status.HTTP_201_CREATED}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please try again later!") 