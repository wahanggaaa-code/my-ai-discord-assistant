import discord
from discord.ext import commands
from config import DISCORD_BOT_TOKEN
from ai_handler import get_ai_response, generate_image
from views import MainPanelControlView, EndSessionView, ImageSettingsView

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # DAFTARKAN SEMUA VIEW PERMANEN
    bot.add_view(MainPanelControlView())
    bot.add_view(EndSessionView())
    bot.add_view(ImageSettingsView())
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Gemini & Groq AI 🤖 | !setup_panel"))
    print(f'✅ Bot aktif & terhubung sebagai {bot.user.name}')

@bot.command(name="setup_panel")
@commands.has_permissions(administrator=True)
async def setup_panel(ctx):
    view = MainPanelControlView()
    await ctx.send(
        content=(
            "🤖 **AI AUTOMATION PANEL (GEMINI + GROQ DUAL ENGINE)**\n"
            "Pilih layanan AI yang ingin Anda gunakan di bawah ini:\n"
            "• **💬 Chat AI (Teks):** Bebas pilih Gemini / Groq (Llama 3.3, DeepSeek R1).\n"
            "• **🎨 Generate Gambar AI:** Atur Gaya & Ukuran Gambar privat."
        ),
        view=view
    )
    await ctx.message.delete()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # A. CHAT TEKS PRIVAT (Thread 'ai-')
    if isinstance(message.channel, discord.Thread) and message.channel.name.startswith("ai-"):
        prompt = message.content.strip()
        if not prompt: return

        async with message.channel.typing():
            try:
                reply_text = get_ai_response(message.channel.id, prompt)

                # PEMOTONG PESAN > 2000 KARAKTER
                if len(reply_text) > 2000:
                    for i in range(0, len(reply_text), 1900):
                        await message.channel.send(reply_text[i:i+1900])
                else:
                    await message.channel.send(reply_text)

            except Exception as e:
                await message.channel.send(f"⚠️ Error: {e}")

    # B. GENERATE GAMBAR PRIVAT (Thread 'draw-')
    elif isinstance(message.channel, discord.Thread) and message.channel.name.startswith("draw-"):
        prompt = message.content.strip()
        if not prompt: return

        msg = await message.channel.send(f"🎨 **Memproses gambar untuk:** *\"{prompt}\"*...")
        async with message.channel.typing():
            try:
                status_title, picture = await generate_image(message.channel.id, prompt)
                if picture:
                    await msg.delete()
                    await message.channel.send(content=f"🖼️ Hasil untuk: **{prompt}** (oleh {message.author.mention})", file=picture)
                else:
                    await msg.edit(content="⚠️ Gagal mengunduh gambar dari AI Generator.")
            except Exception as e:
                await msg.edit(content=f"⚠️ Error: {e}")

    await bot.process_commands(message)

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Web Server Mini agar Render Web Service Free Tier ($0/bulan) Bisa Aktif
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is online and healthy!")

def run_web_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# Jalankan Web Server di latar belakang
threading.Thread(target=run_web_server, daemon=True).start()

# JALANKAN BOT
if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
