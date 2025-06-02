import json
import os
# from fastapi import HTTPException, status
from google import genai
from pathlib import Path
from pydantic import BaseModel

class Medicine(BaseModel):
    name:str
    quantity:str
    power:str
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
f = open(Path("prompts/general.txt"),"r")
f1 = open(Path("prompts/json_prompt.txt"),"r")
system_prompt = f.read()
json_conversion_prompt = f1.read()

async def medical_grocery_chat(prompt: str,media_image:str = None):
    try:
        if media_image and prompt == None:
            file_ref = client.files.upload(file=media_image)
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-04-17",
                config={
                    'response_mime_type': 'application/json',
                    "response_schema":list[Medicine]
                },
                contents=[json_conversion_prompt,
              file_ref]
            )
            
            cleaned_dict_list = [med.model_dump() for med in response.parsed]

            return cleaned_dict_list
        elif prompt and media_image:
            file_ref = client.files.upload(file=media_image)
            
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-04-17",
                contents=[f"{prompt}. Explain the user about the medical or grocery information provided in the image in the easiest possible manner.",
              file_ref]
            )
            return response.text
            
        else:
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=
                f"""
            Make decisions based on this (Also remember not to show your internal thoughts to the user): {system_prompt}
            and here is the question:
            {prompt}"""
                )
        return response.text
    except Exception as e:
        
        return {"error": str(e)}  # ✅ Still a generator in case of error
