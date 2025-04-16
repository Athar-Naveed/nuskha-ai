import os
# from fastapi import HTTPException, status
from google import genai
from pathlib import Path


client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
async def medical_grocery_chat(prompt: str,media_image:str = None):
    try:
        if media_image and prompt == None:
            file_ref = client.files.upload(file=media_image)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=["Extract only the medicine or product name and power (remember mg is the power of the medicine), keep the quantity 1 (never forget). And return the contents of the image in json format",
              file_ref]
            )
            return response.text
        elif prompt and media_image:
            file_ref = client.files.upload(file=media_image)
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[f"{prompt}. Explain the user about the medical or grocery information provided in the image in the easiest possible manner.",
              file_ref]
            )
            return response.text
            
        else:
            with open(Path("prompts/general.txt"),"r") as f:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=
                    f"""
                Make decisions based on this (Also remember not to show your internal thoughts to the user): {f.read()}
                and here is the question:
                {prompt}"""
                    )
            return response.text
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}  # ✅ Still a generator in case of error

