import os
from fastapi import HTTPException, status
import google.generativeai as genai



genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel("gemini-1.5-pro")

async def medical_grocery_chat(prompt:str):
    
    try:
        with open("prompts/general.txt","r") as f:
            response = await model.generate_content_async(
                f"""
            Make decisions based on this: {f.read()}
            and here is the question:
            {prompt}"""
                )
            if hasattr(response, "to_dict"):
                response_data = response.to_dict()  # Use `to_dict` if available
            elif isinstance(response, dict):
                response_data = response
            else:
                response_data = str(response)  # Fallback to string representation
            
            return {response_data['candidates'][0]['content']['parts'][0]['text']}
    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail={"error":f"Error! {e}","status":status.HTTP_500_INTERNAL_SERVER_ERROR})