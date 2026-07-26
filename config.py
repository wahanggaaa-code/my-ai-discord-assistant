import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# 🎭 DAFTAR PILIHAN MESIN & MODEL AI
AI_MODELS = {
    "gemini_flash": {
        "name": "♊ Gemini Flash",
        "engine": "gemini",
        "model_id": "gemini-flash-latest",
        "system_prompt": "Kamu adalah AI Assistant Gemini yang ramah, cerdas, dan membantu di server ini. Jawablah dengan bahasa Indonesia yang santai, sopan, dan jelas."
    },
    "groq_llama70b": {
        "name": "🦙 Groq - Llama 3.3 70B",
        "engine": "groq",
        "model_id": "llama-3.3-70b-versatile",
        "system_prompt": "Kamu adalah Llama 3.3 70B yang dijalankan oleh chip super cepat Groq LPU. Kamu sangat cerdas, responsif, dan membantu di server ini. Jawablah dengan bahasa Indonesia yang ramah dan akurat."
    },
    "groq_deepseek": {
        "name": "🧠 Groq - Llama 3.3 70B (Logika)",
        "engine": "groq",
        "model_id": "llama-3.3-70b-versatile", # <-- Diganti ke model Llama 3.3 70B yang aktif
        "system_prompt": "Kamu adalah AI yang sangat cerdas. Kamu sangat unggul dalam penalaran logika, pemecahan masalah, dan matematika. Berikan jawaban yang terstruktur dan jelas dalam bahasa Indonesia."
    },

    "groq_fast": {
        "name": "⚡ Groq - Llama 3.1 Instant",
        "engine": "groq",
        "model_id": "llama-3.1-8b-instant",
        "system_prompt": "Kamu adalah AI ultra-cepat berkecepatan tinggi. Jawablah dengan ringkas, padat, dan ramah dalam bahasa Indonesia."
    },
    "groq_coding": {
        "name": "🧑‍💻 Groq - Tutor Coding",
        "engine": "groq",
        "model_id": "llama-3.3-70b-versatile",
        "system_prompt": "Kamu adalah Senior Software Engineer & Tutor Coding. Jawablah pertanyaan pemrograman secara terstruktur, jelaskan logikanya, dan berikan contoh kode yang bersih dan aman."
    },
    "gemini_curhat": {
        "name": "🛋️ Gemini - Teman Curhat",
        "engine": "gemini",
        "model_id": "gemini-flash-latest",
        "system_prompt": "Kamu adalah Teman Curhat yang sangat empatetik, hangat, pendengar yang baik, dan suportif. Berikan respon yang menenangkan dan ramah ala sahabat dekat."
    }
}

# 🎨 DAFTAR GAYA GAMBAR
STYLE_PROMPTS = {
    "Biasa": "",
    "Anime": ", anime style, highly detailed Japanese animation, vibrant colors, studio ghibli aesthetic",
    "Cyberpunk": ", cyberpunk style, neon lights, futuristic city, highly detailed 8k, cinematic lighting",
    "Photorealistic": ", photorealistic, 8k resolution, ultra realistic photo, professional photography",
    "3D Render": ", 3d render style, blender 3d, pixar style, octane render, smooth lighting"
}

# 📐 DAFTAR UKURAN GAMBAR
RATIO_DIMENSIONS = {
    "1:1 (Persegi)": (1024, 1024),
    "16:9 (Landscape)": (1280, 720),
    "9:16 (Portrait/Story)": (720, 1280)
}

# Tempat Menyimpan Memori Chat & Setting Gambar
thread_chats = {}
image_thread_settings = {}