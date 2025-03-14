import os
from fastapi import HTTPException, status
from google import genai
from google.genai import types
from pathlib import Path


client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
images_url = os.getenv("DEVELOPMENT_URL")
async def medical_grocery_chat(prompt: str,media_image:str = None):
    
    try:
        print(f"media_image: {media_image}")
        file_ref = client.files.upload(file=media_image)
        print(f'{file_ref=}')
        if media_image:
            # Case: Only image is provided
            # with open(Path("prompts/general.txt"), "r") as f:
            #     base_prompt = f.read()  # Optional: Use this if needed
            print("working?")
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=["What can you tell me about these instruments?",
              file_ref]
            )
            print(f"response: {response}")
            return response.text
        elif prompt and media_image:
            pass
        else:
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








# when we will start streaming on mobile this code will be used
            # with open("prompts/general.txt", "r") as f:
            #     response = await model.generate_content_async(
            #         f"""
            #         Make decisions based on this: {f.read()}
            #         and here is the question:
            #         {prompt}"""
            #     ,stream=True)  # ✅ Streaming response
            #     async for chunk in response:
            #         yield chunk.text