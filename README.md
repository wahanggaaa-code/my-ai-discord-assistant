# 🤖 My AI Discord Assistant (Triple-Engine AI)

**My AI Discord Assistant** adalah Bot Discord AI Multi-Engine modern yang menggabungkan 3 kekuatan AI raksasa sekaligus: **Google Gemini API**, **Groq LPU (Llama 3.3 70B & Llama 3.1 Instant)**, dan **OpenRouter AI Auto-Router**, serta generator gambar gratis dari **Pollinations AI**.

Bot ini menggunakan sistem **Automation Panel (Private Threads)** sehingga setiap obrolan bersifat privat, rahasia, dan secara otomatis mengirimkan rekap obrolan ke DM (*Direct Message*) pengguna ketika sesi diakhiri.

---

## ✨ Fitur-Fitur Utama

* ♊ **Google Gemini API:** Mendukung model *Gemini Flash* untuk tanya-jawab umum & mode *Teman Curhat* yang empatetik.
* 🦙 **Groq LPU (Ultra-Fast Inference):** Pemrosesan super kilat (< 0.2 detik) menggunakan model *Llama 3.3 70B* (Cerdas & Logika) dan *Llama 3.1 Instant*.
* 💻 **OpenRouter AI Integration:** Menggunakan *Auto-Router* pintar (`openrouter/free`) yang selalu terhubung ke model AI gratisan terbaru dan terbaik.
* 🎨 **AI Image Generator (Pollinations AI):** Hasilkan gambar/artwork gratis tanpa limit dengan pilihan **Style Art** (*Anime*, *Cyberpunk*, *Photorealistic*, *3D Render*) dan **Aspect Ratio** (*1:1*, *16:9*, *9:16*).
* 🔒 **Sistem Ruang Privat Otomatis (Private Threads):** Ruang chat khusus dibuat otomatis saat member menekan tombol di panel utama.
* 📜 **Rekap Obrolan via DM:** Saat tombol **🔴 Akhiri Sesi** diklik, bot merangkum seluruh percakapan dan mengirimkannya secara rahasia ke DM pengguna sebelum menghapus ruang privat tersebut.
* ⚡ **Optimasi Memori (Lazy Loading):** Menggunakan teknik pemuatan memori pintar sehingga penggunaan RAM hanya ~30 MB, 100% stabil berjalan di plan gratisan [Discloud](https://discloudbot.com/) (100 MB RAM limit).
* 📦 **Arsitektur Modular:** Kode bersih terpisah menjadi `config.py`, `ai_handler.py`, `views.py`, dan `main.py`.

---

## 📁 Struktur Proyek

```text
my-ai-discord-assistant/
│
├── .env                  # Tempat Kunci API & Token Bot (Privat / Jangan di-push ke public repo)
├── requirements.txt      # Daftar library Python
├── discloud.config       # Konfigurasi hosting Discloud (100 MB RAM)
├── config.py             # Konfigurasi Model AI, System Prompts, & Gaya Gambar
├── ai_handler.py         # Logika pemicu Gemini, Groq, OpenRouter, & Pollinations
├── views.py              # Komponen UI Discord (Panel Utama, Buttons, Dropdowns)
└── main.py               # File utama untuk menjalankan bot
```

---

## 🔑 Kunci API & Lingkungan (`.env`)

Buat file bernama `.env` di dalam folder proyek Anda, lalu isikan **API KEY** Anda:

```env
GEMINI_API_KEY=masukkan_gemini_api_key_anda
GROQ_API_KEY=masukkan_groq_api_key_anda
OPENROUTER_API_KEY=masukkan_openrouter_api_key_anda
DISCORD_BOT_TOKEN=masukkan_discord_bot_token_anda
```

> 💡 **Di mana mendapatkan kunci API gratis?**
> * **Gemini API Key:** [Google AI Studio](https://aistudio.google.com/)
> * **Groq API Key:** [Groq Cloud Console](https://console.groq.com/)
> * **OpenRouter API Key:** [OpenRouter.ai](https://openrouter.ai/)
> * **Discord Bot Token:** [Discord Developer Portal](https://discord.com/developers/applications) *(Pastikan mengaktifkan **Message Content Intent**)*

---

## 🚀 Cara Pemasangan (Lokal di PC / Laptop)

### 1. Clone Repositori
```bash
git clone https://github.com/wahanggaaa-code/my-ai-discord-assistant.git
cd my-ai-discord-assistant
```

### 2. Install Library
```bash
pip install -r requirements.txt
```

### 3. Jalankan Bot
```bash
python main.py
```

### 4. Setup Panel di Server Discord
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
5. Bot Anda akan langsung **Online 24/7** di server cloud tanpa terkena error OOM!

---

## 📜 Lisensi & Kontribusi

Proyek ini bersifat **Open Source**. Silakan lakukan *Fork*, beri *Star* 🌟, atau modifikasi sesuai kebutuhan server Anda!

Dibuat dengan ❤️ oleh **[wahanggaaa](https://github.com/wahanggaaa-code)**.
