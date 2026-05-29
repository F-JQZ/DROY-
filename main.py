import discord
from discord import app_commands  
from discord.ext import commands
from discord.ui import View, Modal, TextInput
import os

# إعداد الـ Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True 
allowed_mentions = discord.AllowedMentions(everyone=True, roles=True, users=True)

bot = commands.Bot(command_prefix="/", intents=intents, allowed_mentions=allowed_mentions)

# ⚙️ الإعدادات
MY_GUILD_ID = 1502777009087185056 
TARGET_CHANNEL_ID = 1508308686932803715 
SEPARATOR_IMAGE_URL = "https://i.ibb.co/v4d715H/1c4e2c245ccd1c7b7736d3509b6e919f.webp"

# ==========================================
# ⭐ نظام التقييم
# ==========================================
class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="تقديم تقييم للمتجر")
        self.stars_input = TextInput(label="عدد النجوم (من 1 إلى 5)", placeholder="اكتب رقم من 1 إلى 5 فقط...", min_length=1, max_length=1, required=True)
        self.add_item(self.stars_input)
        self.comment_input = TextInput(label="اكتب تقييمك هنا", style=discord.TextStyle.paragraph, placeholder="اكتب رأيك بالخدمة أو المنتج...", min_length=3, max_length=500, required=True)
        self.add_item(self.comment_input)

    async def on_submit(self, interaction: discord.Interaction):
        stars_text = self.stars_input.value.strip()
        comment = self.comment_input.value
        stars_number = int(stars_text)
        stars_emojis = "⭐" * stars_number
        embed = discord.Embed(title="✨ شكراً على تقييمك!", description=f"\n```\n• {comment}\n```", color=0x808080)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="⭐ تقييم الخدمة :", value=stars_emojis, inline=True)
        embed.add_field(name="📦 المنتج :", value="خدمة / منتج من المتجر", inline=True)
        embed.set_footer(text="Droy Store - نظام التقييمات")
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("✅ تم إرسال تقييمك بنجاح، شكراً لك!", ephemeral=True)

class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="اضغط هنا للتقييم", style=discord.ButtonStyle.green, emoji="📝", custom_id="review_btn")
    async def open_feedback_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal())

# ==========================================
# 🚀 نظام المتجر (تم إصلاح تداخل النصوص هنا)
# ==========================================
class StoreView(View):
    def __init__(self, details, c_id):
        super().__init__(timeout=None)
        self.details = details
        self.show_details.custom_id = c_id

    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.details, ephemeral=True)

@bot.tree.command(name="send_review", description="يرسل رسالة التقييم الثابتة")
async def send_review(interaction: discord.Interaction):
    embed = discord.Embed(title="⭐ نظام تقييمات Droy Store", description="عزيزي العميل، يسعدنا سماع رأيك في خدماتنا!\n\nاضغط على الزر بالأسفل لتقديم تقييمك.", color=0x5c3a75)
    await interaction.response.send_message("✅ تم الإرسال!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=FeedbackView())

@bot.tree.command(name="send_shop", description="يرسل متجر البوستات")
async def send_shop(interaction: discord.Interaction):
    text = ("# **تم تـ9فير بـ0ستات**\n\n**1 M0nth**\n**14 b00st**\n**~~22SAR~~**\n\n**3 M0nth**\n**14 b00st**\n**~~44SAR~~**\n\n**السعر الحالي**\n\n**1 M0nth**\n**14 b00st**\n**14SAR**\n\n**3 M0nth**\n**14 b00st**\n**22SAR**\n\n\n||@here @everyone||")
    embed = discord.Embed(title="🎁 البوستات", description="اضغط الزر بالأسفل لكامل التفاصيل", color=0x808080)
    embed.set_image(url=SEPARATOR_IMAGE_URL)
    await interaction.response.send_message("✅ تم!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=StoreView(text, "boost_btn_id"))

@bot.tree.command(name="send_nitro", description="يرسل متجر النيترو")
async def send_nitro(interaction: discord.Interaction):
    text = ("# **تم تـ9فير نيتر9 Gift**\n\n**Nitr0 M0nth**\n**12SAR**\n\n||@here @everyone||")
    embed = discord.Embed(title="🎁 نيترو", description="اضغط الزر بالأسفل لكامل التفاصيل", color=0x808080)
    embed.set_image(url=SEPARATOR_IMAGE_URL)
    await interaction.response.send_message("✅ تم!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=StoreView(text, "nitro_btn_id"))

# ==========================================
# ✅ تشغيل البوت
# ==========================================
@bot.event
async def on_message(message):
    if message.author == bot.user: return
    if TARGET_CHANNEL_ID != 0 and message.channel.id == TARGET_CHANNEL_ID:
        embed = discord.Embed(color=message.author.color)
        embed.set_image(url=SEPARATOR_IMAGE_URL)
        await message.channel.send(embed=embed)
    await bot.process_commands(message)

@bot.event
async def on_ready():
    bot.add_view(FeedbackView())
    bot.add_view(StoreView("", "boost_btn_id"))
    bot.add_view(StoreView("", "nitro_btn_id"))
    try:
        guild = discord.Object(id=MY_GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
    except: pass
    print(f'✅ تم تشغيل البوت: {bot.user}')
    await bot.change_presence(activity=discord.Game(name="SL6E"))

TOKEN = os.environ.get('DISCORD_TOKEN')
if __name__ == "__main__":
    bot.run(TOKEN)
