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

bot = commands.Bot(command_prefix="/", intents=intents)

# ⚙️ الإعدادات (ضع الآيديهات الخاصة بك هنا)
MY_GUILD_ID = 1502777009087185056 
IMAGE_URL = "https://i.ibb.co/v4d715H/1c4e2c245ccd1c7b7736d3509b6e919f.webp"

# ==========================================
# ⭐ نظام التقييم
# ==========================================
class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="تقديم تقييم لـ Droy Store")
        self.stars_input = TextInput(label="عدد النجوم (1-5)", placeholder="اكتب رقم من 1 إلى 5...", min_length=1, max_length=1)
        self.add_item(self.stars_input)
        self.comment_input = TextInput(label="اكتب تقييمك", style=discord.TextStyle.paragraph)
        self.add_item(self.comment_input)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="✨ تقييم جديد", description=f"**التقييم:** {'⭐'*int(self.stars_input.value)}\n**الرأي:** {self.comment_input.value}", color=0x808080)
        embed.set_thumbnail(url=IMAGE_URL)
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("✅ تم إرسال تقييمك!", ephemeral=True)

class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="اضغط هنا للتقييم", style=discord.ButtonStyle.green, emoji="📝", custom_id="review_btn")
    async def open_feedback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal())

# ==========================================
# 🎁 متجر البوستات والنيترو (مصحح)
# ==========================================
class StoreView(View):
    def __init__(self, details, custom_id):
        super().__init__(timeout=None)
        self.details = details
        self.show_details_button.custom_id = custom_id

    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.details, ephemeral=True)

# أمر البوستات
@bot.tree.command(name="send_shop", description="إرسال متجر البوستات")
async def send_shop(interaction: discord.Interaction):
    boost_text = (
        "# **تم توفير بوستات**\n\n"
        "**1 Month**\n**14 boost**\n**~~22SAR~~**\n\n"
        "**3 Month**\n**14 boost**\n**~~44SAR~~**\n\n"
        "**السعر الحالي**\n\n"
        "**1 Month** - **14SAR**\n"
        "**3 Month** - **22SAR**\n\n"
        "||@everyone||"
    )
    embed = discord.Embed(title="🎁 بوستات Droy Store", description="اضغط الزر بالأسفل لكامل التفاصيل", color=0x5c3a75)
    embed.set_image(url=IMAGE_URL)
    await interaction.response.send_message("تم الإرسال", ephemeral=True)
    await interaction.channel.send(embed=embed, view=StoreView(boost_text, "boost_btn_unique"))

# أمر النيترو
@bot.tree.command(name="send_nitro", description="إرسال متجر النيترو")
async def send_nitro(interaction: discord.Interaction):
    nitro_text = (
        "# **تم توفير نيترو Gift**\n\n"
        "**Nitro Month**\n"
        "**12SAR**\n\n"
        "||@everyone||"
    )
    embed = discord.Embed(title="🎁 نيترو Droy Store", description="اضغط الزر بالأسفل لكامل التفاصيل", color=0x5c3a75)
    embed.set_image(url=IMAGE_URL)
    await interaction.response.send_message("تم الإرسال", ephemeral=True)
    await interaction.channel.send(embed=embed, view=StoreView(nitro_text, "nitro_btn_unique"))

# ==========================================
# ✅ تشغيل البوت
# ==========================================
@bot.event
async def on_ready():
    # تسجيل الـ Views (أضف هنا أي views إضافية لديك مثل التكتات)
    bot.add_view(FeedbackView())
    bot.add_view(StoreView("", "boost_btn_unique"))
    bot.add_view(StoreView("", "nitro_btn_unique"))
    
    try:
        guild = discord.Object(id=MY_GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        print(f"⚙️ تم مزامنة {len(synced)} أمر بنجاح!")
    except Exception as e:
        print(f"❌ فشل المزامنة: {e}")
        
    print(f'✅ تم تشغيل البوت: {bot.user}')
    await bot.change_presence(activity=discord.Game(name="SL6E"))

TOKEN = os.environ.get('DISCORD_TOKEN')
if __name__ == "__main__":
    bot.run(TOKEN)
