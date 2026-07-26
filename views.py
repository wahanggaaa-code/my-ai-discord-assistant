import discord
import asyncio
from config import AI_MODELS, image_thread_settings, thread_chats
from ai_handler import init_thread_session

# ==============================================================================
# TOMBOL AKHIRI SESI & REKAP DM
# ==============================================================================
class EndSessionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔴 Akhiri Sesi", style=discord.ButtonStyle.danger, custom_id="btn_end_ai_session_v2")
    async def end_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🧹 **Menyiapkan rekap obrolan & menutup sesi...**", ephemeral=False)

        conversation = []
        async for msg in interaction.channel.history(limit=100, oldest_first=True):
            if msg.content.strip():
                sender = "👤 Anda" if msg.author.id == interaction.user.id else "🤖 AI"
                conversation.append(f"**{sender}:** {msg.content}")

        history_text = "\n\n".join(conversation) if conversation else "Tidak ada percakapan tercatat."
        if len(history_text) > 3800:
            history_text = history_text[:3800] + "\n\n*(catatan terpotong karena terlalu panjang)*"

        session_type = "🎨 Generate Gambar" if interaction.channel.name.startswith("draw-") else "💬 Chat Teks AI"

        embed = discord.Embed(
            title="📜 Rekap Sesi AI Pribadi Anda",
            description=f"**📍 Tipe Sesi:** {session_type}\n**📍 Ruang:** `{interaction.channel.name}`\n\n---\n\n{history_text}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text="Salinan ini hanya dikirimkan khusus kepada Anda secara rahasia.")

        try:
            await interaction.user.send(embed=embed)
        except Exception as e:
            print(f"⚠️ Error DM: {e}")

        if interaction.channel.id in thread_chats: del thread_chats[interaction.channel.id]
        if interaction.channel.id in image_thread_settings: del image_thread_settings[interaction.channel.id]

        await asyncio.sleep(2)
        await interaction.channel.delete()


# ==============================================================================
# SETTING GAMBAR (GAYA & UKURAN)
# ==============================================================================
class ImageSettingsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="🎨 Pilih Gaya Art Gambar...",
        custom_id="select_image_style",
        options=[
            discord.SelectOption(label="Biasa / Default", value="Biasa", emoji="🖼️"),
            discord.SelectOption(label="Anime Style", value="Anime", emoji="⛩️"),
            discord.SelectOption(label="Cyberpunk Futuristic", value="Cyberpunk", emoji="🏙️"),
            discord.SelectOption(label="Photorealistic (Foto Asli)", value="Photorealistic", emoji="📸"),
            discord.SelectOption(label="3D Render (Pixar/Blender)", value="3D Render", emoji="🧊"),
        ]
    )
    async def select_style(self, interaction: discord.Interaction, select: discord.ui.Select):
        thread_id = interaction.channel.id
        if thread_id not in image_thread_settings: image_thread_settings[thread_id] = {'style': 'Biasa', 'ratio': '1:1 (Persegi)'}
        image_thread_settings[thread_id]['style'] = select.values[0]
        await interaction.response.send_message(f"✅ Gaya gambar diubah menjadi: **{select.values[0]}**", ephemeral=True)

    @discord.ui.select(
        placeholder="📐 Pilih Ukuran Gambar...",
        custom_id="select_image_ratio",
        options=[
            discord.SelectOption(label="1:1 (Persegi - Default)", value="1:1 (Persegi)", emoji="⏹️"),
            discord.SelectOption(label="16:9 (Landscape / Banner)", value="16:9 (Landscape)", emoji="🖼️"),
            discord.SelectOption(label="9:16 (Portrait / Story HP)", value="9:16 (Portrait/Story)", emoji="📱"),
        ]
    )
    async def select_ratio(self, interaction: discord.Interaction, select: discord.ui.Select):
        thread_id = interaction.channel.id
        if thread_id not in image_thread_settings: image_thread_settings[thread_id] = {'style': 'Biasa', 'ratio': '1:1 (Persegi)'}
        image_thread_settings[thread_id]['ratio'] = select.values[0]
        await interaction.response.send_message(f"✅ Ukuran gambar diubah menjadi: **{select.values[0]}**", ephemeral=True)


# ==============================================================================
# DROPDOWN PILIHAN MODEL AI
# ==============================================================================
class AIModelSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.select(
        placeholder="🧠 Pilih Mesin & Model AI...",
        options=[
            discord.SelectOption(label="Gemini Flash (Google)", value="gemini_flash", description="Asisten Umum Cerdas Multi-Topik", emoji="♊"),
            discord.SelectOption(label="Groq - Llama 3.3 70B (Meta)", value="groq_llama70b", description="Model Terpandai Meta di Chip Groq", emoji="🦙"),
            discord.SelectOption(label="Groq - DeepSeek R1", value="groq_deepseek", description="Pakar Logika & Penalaran", emoji="🧠"),
            discord.SelectOption(label="Groq - Llama 3.1 Instant", value="groq_fast", description="Respon Kilat < 0.2 Detik", emoji="⚡"),
            discord.SelectOption(label="Groq - Tutor Coding", value="groq_coding", description="Pakar Pemrograman", emoji="🧑‍💻"),
            discord.SelectOption(label="Gemini - Teman Curhat", value="gemini_curhat", description="Empati Tinggi & Suportif", emoji="🛋️"),
        ]
    )
    async def select_model(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.defer(ephemeral=True)
        chosen_key = select.values[0]
        model_info = AI_MODELS.get(chosen_key)

        thread_name = f"ai-{interaction.user.name}"
        try:
            thread = await interaction.channel.create_thread(
                name=thread_name,
                type=discord.ChannelType.private_thread,
                auto_archive_duration=60
            )
            await thread.add_user(interaction.user)

            init_thread_session(thread.id, chosen_key)

            end_view = EndSessionView()
            await thread.send(
                content=(
                    f"👋 **Selamat Datang {interaction.user.mention}!**\n"
                    f"Ruang chat privat telah dibuat menggunakan mesin: **{model_info['name']}**.\n"
                    f"Silakan bertanya apa saja di sini!\n\n"
                    f"Jika sudah selesai, klik tombol **Akhiri Sesi** di bawah:"
                ),
                view=end_view
            )
            await interaction.followup.send(content=f"✅ Ruang Chat Teks (**{model_info['name']}**) berhasil dibuat: {thread.mention}", ephemeral=True)

        except Exception as e:
            await interaction.followup.send(content=f"⚠️ Error membuat ruang chat: {e}", ephemeral=True)


# ==============================================================================
# PANEL UTAMA CONTROLLER
# ==============================================================================
class MainPanelControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="💬 Chat AI (Teks)", style=discord.ButtonStyle.success, custom_id="btn_create_text_ai_v2")
    async def create_text_chat(self, interaction: discord.Interaction, button: discord.ui.Button):
        select_view = AIModelSelectView()
        await interaction.response.send_message(content="🎭 **Pilih Mesin / Model AI yang ingin Anda ajak ngobrol:**", view=select_view, ephemeral=True)

    @discord.ui.button(label="🎨 Generate Gambar AI", style=discord.ButtonStyle.primary, custom_id="btn_create_image_ai_v2")
    async def create_image_chat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        thread_name = f"draw-{interaction.user.name}"
        try:
            thread = await interaction.channel.create_thread(
                name=thread_name,
                type=discord.ChannelType.private_thread,
                auto_archive_duration=60
            )
            await thread.add_user(interaction.user)

            image_thread_settings[thread.id] = {'style': 'Biasa', 'ratio': '1:1 (Persegi)'}

            end_view = EndSessionView()
            settings_view = ImageSettingsView()

            await thread.send(
                content=(
                    f"🎨 **Selamat Datang {interaction.user.mention}!**\n"
                    f"Ini adalah ruang privat pembuatan gambar AI.\n"
                    f"Ketik deskripsi gambar apa saja di sini, dan AI akan otomatis membuatkan gambarnya untuk Anda!\n\n"
                    f"⚙️ *Gunakan Menu Dropdown di bawah jika ingin mengubah Gaya Art atau Ukuran Gambar:*"
                ),
                view=settings_view
            )
            await thread.send(content="🔴 *Klik tombol di bawah jika ingin mengakhiri sesi:*", view=end_view)

            await interaction.followup.send(content=f"✅ Ruang Generate Gambar berhasil dibuat: {thread.mention}", ephemeral=True)

        except Exception as e:
            await interaction.followup.send(content=f"⚠️ Error membuat ruang gambar: {e}", ephemeral=True)