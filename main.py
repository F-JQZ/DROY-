import os
import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput
from discord import app_commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
allowed_mentions = discord.AllowedMentions(everyone=True, roles=True, users=True)
bot = commands.Bot(command_prefix="!", intents=intents, allowed_mentions=allowed_mentions)

# ==========================================
# ⚙️ الإعدادات
# ==========================================
TARGET_CHANNEL_ID = 0  
BANNER_URL = "ضع_رابط_الصورة_المباشر_هنا" 

# ==========================================
# ⭐ نظام التقييم
# ==========================================
class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="تقديم تقييم للمتجر")
        self.stars_input = TextInput(label="عدد النجوم (من 1 إلى 5)", placeholder="اكتب رقم من 1 إلى 5...", min_length=1, max_length=1, required=True)
        self.add_item(self.stars_input)
        self.comment_input = TextInput(label="اكتب تقييمك هنا", style=discord.TextStyle.paragraph, placeholder="اكتب رأيك...", min_length=3, max_length=500, required=True)
        self.add_item(self.comment_input)

    async def on_submit(self, interaction: discord.Interaction):
        stars_text = self.stars_input.value.strip()
        if not stars_text.isdigit() or not (1 <= int(stars_text) <= 5):
            await interaction.response.send_message("❌ خطأ: يجب كتابة رقم من 1 إلى 5!", ephemeral=True)
            return
        
        embed = discord.Embed(title="✨ شكراً على تقييمك!", description=f"```• {self.comment_input.value}```", color=0x5c3a75)
        embed.add_field(name="⭐ تقييم الخدمة :", value="⭐" * int(stars_text), inline=True)
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("✅ تم الإرسال!", ephemeral=True)

class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="اضغط هنا للتقييم", style=discord.ButtonStyle.green, emoji="📝")
    async def open_feedback_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal())

# ==========================================
# 🚀 متجر البوستات والنيترو
# ==========================================
class BoostView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("# **تم تـ9فير بـ0ستات**\n14 b00st = 14SAR", ephemeral=True)

class NitroView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("# **تم تـ9فير نيتر9 Gift**\nNitr0 M0nth = 12SAR", ephemeral=True)

# ==========================================
# 📋 الأوامر المحدثة
# ==========================================
@bot.tree.command(name="send_review", description="يرسل رسالة التقييم")
async def send_review(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(title="⭐ نظام تقييمات Droy Store", description="اضغط الزر بالأسفل لتقديم تقييمك.", color=0x5c3a75)
    embed.set_image(url=BANNER_URL)
    await interaction.followup.send(embed=embed, view=FeedbackView())

@bot.tree.command(name="send_shop", description="يرسل متجر البوستات")
async def send_shop(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(title="🎁 بـوستات", description="اضغط الزر بالأسفل لكامل التفاصيل", color=0x99AAB5)
    embed.set_image(url=BANNER_URL)
    await interaction.followup.send(embed=embed, view=BoostView())

@bot.tree.command(name="send_nitro", description="يرسل متجر النيترو")
async def send_nitro(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(title="🎁 نيترو", description="اضغط الزر بالأسفل لكامل التفاصيل", color=0x99AAB5)
    embed.set_image(url=BANNER_URL)
    await interaction.followup.send(embed=embed, view=NitroView())

# ==========================================
# التشغيل
# ==========================================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'✅ يعمل البوت باسم: {bot.user}')

TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(TOKEN)
