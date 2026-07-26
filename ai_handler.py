from google import genai
from google.genai import types
from groq import Groq
import aiohttp
import urllib.parse
import io
import discord
from config import (
    GEMINI_API_KEY, GROQ_API_KEY, AI_MODELS, 
    STYLE_PROMPTS, RATIO_DIMENSIONS, 
    thread_chats, image_thread_settings
)

# Klien AI
gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def init_thread_session(thread_id: int, model_key: str):
    """Menginisialisasi sesi obrolan (Gemini atau Groq)"""
    model_info = AI_MODELS.get(model_key, AI_MODELS["gemini_flash"])
    engine = model_info["engine"]

    if engine == "gemini":
        session = gemini_client.chats.create(
            model=model_info["model_id"],
            config=types.GenerateContentConfig(system_instruction=model_info["system_prompt"])
        )
        thread_chats[thread_id] = {"engine": "gemini", "info": model_info, "session": session}
    elif engine == "groq":
        history = [{"role": "system", "content": model_info["system_prompt"]}]
        thread_chats[thread_id] = {"engine": "groq", "info": model_info, "history": history}
    
    return thread_chats[thread_id]

def get_ai_response(thread_id: int, prompt: str) -> str:
    """Mendapatkan balasan dari Gemini atau Groq"""
    session_data = thread_chats.get(thread_id)
    if not session_data:
        session_data = init_thread_session(thread_id, "gemini_flash")

    engine = session_data["engine"]

    if engine == "gemini":
        response = session_data["session"].send_message(prompt)
        return response.text

    elif engine == "groq":
        session_data["history"].append({"role": "user", "content": prompt})

        completion = groq_client.chat.completions.create(
            model=session_data["info"]["model_id"],
            messages=session_data["history"],
            temperature=0.7,
            max_tokens=2048,
        )
        reply_text = completion.choices[0].message.content
        session_data["history"].append({"role": "assistant", "content": reply_text})
        return reply_text

async def generate_image(thread_id: int, prompt: str) -> tuple[str, discord.File]:
    """Menghasilkan gambar dari Pollinations AI"""
    settings = image_thread_settings.get(thread_id, {'style': 'Biasa', 'ratio': '1:1 (Persegi)'})
    style_text = STYLE_PROMPTS.get(settings['style'], "")
    width, height = RATIO_DIMENSIONS.get(settings['ratio'], (1024, 1024))
    full_prompt = f"{prompt}{style_text}"

    prompt_encoded = urllib.parse.quote(full_prompt)
    image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width={width}&height={height}&nologo=true"

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as resp:
            if resp.status == 200:
                image_bytes = await resp.read()
                picture = discord.File(io.BytesIO(image_bytes), filename="generated.png")
                status_title = f"🎨 **Membuat Gambar [{settings['style']} | {settings['ratio']}] untuk:** *\"{prompt}\"*"
                return status_title, picture
            return None, None