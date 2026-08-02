import aiohttp
import urllib.parse
import io
import discord
from config import (
    GEMINI_API_KEY, GROQ_API_KEY, OPENROUTER_API_KEY, AI_MODELS, 
    STYLE_PROMPTS, RATIO_DIMENSIONS, 
    thread_chats, image_thread_settings
)

def init_thread_session(thread_id: int, model_key: str):
    """Menginisialisasi sesi obrolan"""
    model_info = AI_MODELS.get(model_key, AI_MODELS["gemini_flash"])
    history = [{"role": "system", "content": model_info["system_prompt"]}]
    
    thread_chats[thread_id] = {
        "info": model_info,
        "history": history
    }
    return thread_chats[thread_id]

async def get_ai_response(thread_id: int, prompt: str) -> str:
    """Mendapatkan balasan AI secara ultra-ringan via HTTP (Sangat Hemat RAM ~30MB)"""
    session_data = thread_chats.get(thread_id)
    if not session_data:
        session_data = init_thread_session(thread_id, "gemini_flash")

    model_info = session_data["info"]
    engine = model_info["engine"]
    model_id = model_info["model_id"]
    
    session_data["history"].append({"role": "user", "content": prompt})

    async with aiohttp.ClientSession() as session:
        # A. MESIN GEMINI
        if engine == "gemini":
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={GEMINI_API_KEY}"
                
                gemini_contents = []
                for h in session_data["history"]:
                    if h["role"] == "system": continue
                    role = "user" if h["role"] == "user" else "model"
                    gemini_contents.append({"role": role, "parts": [{"text": h["content"]}]})

                payload = {
                    "system_instruction": {"parts": [{"text": model_info["system_prompt"]}]},
                    "contents": gemini_contents
                }

                async with session.post(url, json=payload) as resp:
                    data = await resp.json()
                    if resp.status == 200 and "candidates" in data:
                        reply = data["candidates"][0]["content"]["parts"][0]["text"]
                        session_data["history"].append({"role": "assistant", "content": reply})
                        return reply
                    else:
                        raise Exception(f"Gemini Error {resp.status}: {data}")

            except Exception as e:
                print(f"⚠️ Gemini Error ({e}). Fallback ke Groq Llama 3.3...")
                engine = "groq"
                model_id = "llama-3.3-70b-versatile"

        # B. MESIN GROQ
        if engine == "groq":
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
            payload = {
                "model": model_id,
                "messages": session_data["history"],
                "temperature": 0.7,
                "max_tokens": 2048
            }
            async with session.post(url, headers=headers, json=payload) as resp:
                data = await resp.json()
                if resp.status == 200 and "choices" in data:
                    reply = data["choices"][0]["message"]["content"]
                    session_data["history"].append({"role": "assistant", "content": reply})
                    return reply
                else:
                    return f"⚠️ Groq API Error ({resp.status}): {data}"

        # C. MESIN OPENROUTER
        elif engine == "openrouter":
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
            payload = {
                "model": model_id,
                "messages": session_data["history"],
                "temperature": 0.7,
                "max_tokens": 2048
            }
            async with session.post(url, headers=headers, json=payload) as resp:
                data = await resp.json()
                if resp.status == 200 and "choices" in data:
                    reply = data["choices"][0]["message"]["content"]
                    session_data["history"].append({"role": "assistant", "content": reply})
                    return reply
                else:
                    return f"⚠️ OpenRouter Error ({resp.status}): {data}"

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