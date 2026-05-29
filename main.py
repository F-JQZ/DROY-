import os
import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput
from discord import app_commands # ضروري لـ Slash Commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# الإعدادات
SEPARATOR_IMAGE_URL = "https://media.discordapp.net/attachments/1233857597143121920/1245084930121760818/image_2.png"

# --- الفئات (Views) ---
class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="اضغط هنا للتقييم", style=discord.ButtonStyle.green, emoji="📝")
    async def open_feedback_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal())

class BoostView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="عرض التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("تفاصيل البوستات هنا...", ephemeral=True)

class NitroView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="عرض التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("تفاصيل النيترو هنا...", ephemeral=True)

# --- الأوامر المحدثة (Slash Commands) ---

@bot.tree.command(name="send_review", description="يرسل رسالة التقييم")
async def send_review(interaction: discord.Interaction):
    await interaction.response.defer() # <--- الحل هنا يمنع الخطأ
    embed = discord.Embed(title="⭐ نظام تقييمات Droy Store", color=0x5c3a75)
    await interaction.followup.send(embed=embed, view=FeedbackView())

@bot.tree.command(name="send_shop", description="يرسل متجر البوستات")
async def send_shop(interaction: discord.Interaction):
    await interaction.response.defer() # <--- الحل هنا يمنع الخطأ
    embed = discord.Embed(title="🎁 بوسات", color=0xf1c40f)
    embed.set_image(url=SEPARATOR_IMAGE_URL)
    await interaction.followup.send(embed=embed, view=BoostView())

@bot.tree.command(name="send_nitro", description="يرسل متجر النيترو")
async def send_nitro(interaction: discord.Interaction):
    await interaction.response.defer() # <--- الحل هنا يمنع الخطأ
    embed = discord.Embed(title="🎁 نيترو", color=0xf1c40f)
    await interaction.followup.send(embed=embed, view=NitroView())

@bot.event
async def on_ready():
    await bot.tree.sync() # هذا يظهر الأوامر في سيرفرك (قد يحتاج دقيقة للظهور)
    print(f'✅ البوت يعمل: {bot.user}')

TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(TOKEN)
