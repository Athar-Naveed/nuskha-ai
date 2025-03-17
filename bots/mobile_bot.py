import os
# from fastapi import HTTPException, status
from google import genai
# from google.genai import types
from pathlib import Path


client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
# images_url = os.getenv("DEVELOPMENT_URL")
async def medical_grocery_chat(prompt: str,media_image:str = None):
    
    try:
        with open(Path("prompts/general.txt"),"r") as f:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=
                f"""
            Make decisions based on this: {f.read()}
            and here is the question:
            {prompt}"""
                )
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}  # ✅ Still a generator in case of error

