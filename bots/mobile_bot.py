import os
from pathlib import Path
from pydantic import BaseModel
from google import genai
from google.genai import types

class Medicine(BaseModel):
    name: str
    quantity: str
    power: str

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Load prompt templates
system_prompt = Path("prompts/general.txt").read_text()
json_conversion_prompt = Path("prompts/json_prompt.txt").read_text()

# Utility to estimate token count
def estimate_tokens(text: str) -> int:
    # Rough estimation: 1 token ≈ 4 characters (English)
    return len(text) // 4

async def medical_grocery_chat(prompt: str, media_image: str = None):
    try:
        file_ref = None
        if media_image:
            file_ref = client.files.upload(file=media_image)

        # 🧠 Case 1: Image Only → JSON response
        if media_image and not prompt:
            response = client.models.generate_content(
                model="models/gemini-2.0-flash-001",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=list[Medicine]
                ),
                contents=[json_conversion_prompt, file_ref]
            )
            cleaned_dict_list = [med.model_dump() for med in response.parsed]
            return cleaned_dict_list

        # 🧠 Case 2: Prompt + Image → Use cache if content is big enough
        elif prompt and media_image:
            estimated_token_count = estimate_tokens(prompt + json_conversion_prompt)
            use_cache = estimated_token_count >= 4096

            if use_cache:
                cache = client.caches.create(
                    model="models/gemini-2.0-flash-001",
                    config=types.CreateCachedContentConfig(
                        display_name='medical_grocery_cache',
                        system_instruction="You're an expert in analyzing prescription images and answering user queries in simple language.",
                        contents=[file_ref],
                        ttl="4096s"
                    )
                )
                config = types.GenerateContentConfig(cached_content=cache.name)
            else:
                config = None  # No cache config

            response = client.models.generate_content(
                model="models/gemini-2.0-flash-001",
                config=config,
                contents=[
                    f"{prompt}. Explain the user about the medical or grocery information provided in the image in the easiest possible manner.",
                    file_ref
                ]
            )
            return response.text

        # 🧠 Case 3: Prompt Only
        else:
            response = client.models.generate_content(
                model="models/gemini-2.0-flash-001",
                contents=f"""
                    Make decisions based on this (do not reveal your internal thoughts): {system_prompt}
                    and here is the question:
                    {prompt}
                """
            )
            return response.text

    except Exception as e:
        return {"error": str(e)}
