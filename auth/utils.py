import jwt,os,bcrypt
from dotenv import load_dotenv
from fastapi import HTTPException,status

secret_key = os.getenv("SECRET_KEY")

def encoding_jwt_token(user_details):
    try:
        encoded_jwt = jwt.encode(user_details, secret_key, algorithm="HS256")
        return encoded_jwt
    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"message":e,"status":status.HTTP_400_BAD_REQUEST})
    


def decoding_jwt_token(token):
    try:
        decoded_jwt = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded_jwt
    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"message":e,"status":status.HTTP_400_BAD_REQUEST})
    

def hash_password(user_password):
    try:
        hashed_password = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt())
        return hashed_password
    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"message":e,"status":status.HTTP_400_BAD_REQUEST})
    

def verifying_password(hased_password,stored_password):
    try:
        return bcrypt.checkpw(hased_password.encode(), stored_password.encode())
    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"message":e,"status":status.HTTP_400_BAD_REQUEST})
    

