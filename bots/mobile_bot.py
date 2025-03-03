import os
from fastapi import HTTPException, status
import google.generativeai as genai



genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel("gemini-1.5-pro")


async def medical_grocery_chat(prompt: str):
    try:
        with open("prompts/general.txt", "r") as f:
            response = await model.generate_content_async(
                f"""
                Make decisions based on this: {f.read()}
                and here is the question:
                {prompt}"""
            ,stream=True)  # ✅ Streaming response
            async for chunk in response:
                yield chunk.text
            
    except Exception as e:
        print(f"Error: {e}")
        yield {"error": str(e)}  # ✅ Still a generator in case of error
