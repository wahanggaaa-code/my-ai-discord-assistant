# 🤖 My AI Discord Assistant

**My AI Discord Assistant** adalah Bot Discord AI Multi-Engine modern yang menggabungkan kecerdasan **Google Gemini API** dan **Groq LPU (Llama 3.3 70B, DeepSeek R1, Llama 3.1 Instant)**, serta pembuat gambar gratis dari **Pollinations AI**.

Bot ini menggunakan sistem **Automation Panel (Private Threads)** sehingga setiap obrolan bersifat privat, rahasia, dan secara otomatis mengirimkan rekap obrolan ke DM (*Direct Message*) pengguna ketika sesi diakhiri.

---

## ✨ Fitur-Fitur Utama

* ♊ **Google Gemini API:** Mendukung model *Gemini Flash* untuk tanya-jawab umum & mode *Teman Curhat* yang empatetik.
* 🦙 **Groq AI (Ultra Fast Inference):** Pemrosesan super cepat kurang dari 0.2 detik menggunakan model *Llama 3.3 70B*, *DeepSeek R1*, *Llama 3.1 Instant*, dan *Tutor Coding*.
* 🎨 **AI Image Generator (Pollinations AI):** Hasilkan gambar/artwork gratis tanpa limit dengan pilihan **Style Art** (*Anime*, *Cyberpunk*, *Photorealistic*, *3D Render*) dan **Aspect Ratio** (*1:1*, *16:9*, *9:16*).
* 🔒 **Sistem Ruang Privat Otomatis (Private Threads):** Ruang chat khusus dibuat otomatis saat member menekan tombol di panel utama.
* 📜 **Rekap Obrolan via DM:** Saat tombol **🔴 Akhiri Sesi** diklik, bot akan merangkum seluruh percakapan dan mengirimkannya secara rahasia ke DM pengguna sebelum menghapus ruang privat tersebut.
* 📦 **Arsitektur Modular:** Kode bersih terpisah menjadi `config.py`, `ai_handler.py`, `views.py`, dan `main.py`.
* ☁️ **Siap Deploy 24/7 Online:** Dilengkapi file `discloud.config` untuk hosting gratis 24 jam di [Discloud](https://discloudbot.com/).

---

## 📁 Struktur Proyek

```text
my-ai-discord-assistant/
│
├── .env                  # Tempat Kunci API & Token Bot (Privat / Jangan di-push ke repo public)
├── requirements.txt      # Daftar library Python
├── discloud.config       # Konfigurasi hosting Discloud (100 MB RAM)
├── config.py             # Konfigurasi Model AI, System Prompts, & Gaya Gambar
├── ai_handler.py         # Logika pemicu Gemini API, Groq API, & Pollinations
├── views.py              # Komponen UI Discord (Panel Utama, Buttons, Dropdowns)
└── main.py               # File utama untuk menjalankan bot
```

---

## 🚀 Cara Pemasangan (Lokal di PC / Laptop)

### 1. Prasyarat
* Python versi 3.10 atau yang lebih baru.
* Editor Kode (seperti VS Code).

### 2. Clone Repositori
```bash
git clone https://github.com/wahanggaaa-code/my-ai-discord-assistant.git
cd my-ai-discord-assistant
```

### 3. Install Library
Buka terminal di folder proyek, lalu jalankan:
```bash
pip install -r requirements.txt
```

### 4. Buat File `.env`
Buat file bernama `.env` di dalam folder proyek Anda, lalu isikan kunci rahasia Anda:
```env
GEMINI_API_KEY=masukkan_gemini_api_key_anda
GROQ_API_KEY=masukkan_groq_api_key_anda
DISCORD_BOT_TOKEN=masukkan_discord_bot_token_anda
```

> 💡 **Di mana mendapatkan kunci API gratis?**
> * **Gemini API Key:** [Google AI Studio](https://aistudio.google.com/)
> * **Groq API Key:** [Groq Cloud Console](https://console.groq.com/)
> * **Discord Bot Token:** [Discord Developer Portal](https://discord.com/developers/applications) *(Pastikan mengaktifkan **Message Content Intent** di tab Bot)*

### 5. Jalankan Bot
```bash
python main.py
```

### 6. Setup Panel di Server Discord
Masuk ke channel server Discord Anda (sebagai Admin), lalu ketik perintah:
```text
!setup_panel
```
Bot akan memunculkan **AI Automation Panel** interaktif!

---

## ☁️ Cara Deploy 24 Jam Nonstop Gratis (Discloud)

1. Pastikan isi file `discloud.config` Anda seperti ini:
   ```text
   NAME=MyAIBot
   TYPE=bot
   MAIN=main.py
   RAM=100
   AUTORESTART=true
   VERSION=recommended
   ```
2. Blok semua file proyek Anda (`.env`, `main.py`, `config.py`, `ai_handler.py`, `views.py`, `requirements.txt`, `discloud.config`) lalu buat file **`.zip`** (misal: `bot.zip`).
3. Buka [discloudbot.com](https://discloudbot.com/) -> Login dengan akun Discord Anda.
4. Klik **Upload App** / **Unggahan baru** -> Masukkan file `bot.zip`.
5. Bot Anda akan langsung **Online 24/7** di server cloud!

---

## 📜 Lisensi & Kontribusi

Proyek ini bersifat **Open Source**. Silakan lakukan *Fork*, beri *Star* 🌟, atau modifikasi sesuai kebutuhan server Anda!

Dibuat dengan ❤️ oleh **[wahanggaaa](https://github.com/wahanggaaa-code)**.
```
