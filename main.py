import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput
import os

# إعداد الـ Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# ⚙️ الإعدادات
MY_GUILD_ID = 1502777009087185056 
TARGET_CHANNEL_ID = 1508308686932803715 
IMAGE_URL = "https://media.discordapp.net/attachments/1233857597143121920/1245091722830811218/cdf7074f1d9df649.png"

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
# 🎁 نظام المتجر (عام للبوستات والنيترو)
# ==========================================
class StoreView(View):
    def __init__(self, details, c_id):
        super().__init__(timeout=None)
        self.details = details
        self.show_details.custom_id = c_id

    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.details, ephemeral=True)

# ==========================================
# 🚀 الأوامر
# ==========================================

@bot.tree.command(name="send_review", description="إرسال رسالة التقييم")
async def send_review(interaction: discord.Interaction):
    embed = discord.Embed(title="⭐ نظام تقييمات Droy Store", description="اضغط الزر بالأسفل لتقييمنا", color=0x5c3a75)
    embed.set_image(url=IMAGE_URL)
    await interaction.response.send_message("تم الإرسال", ephemeral=True)
    await interaction.channel.send(embed=embed, view=FeedbackView())

@bot.tree.command(name="send_shop", description="إرسال متجر البوستات")
async def send_shop(interaction: discord.Interaction):
    text = "# **تم تـ9فير بـ0ستات**\n\n**1 M0nth**\n**14 b00st**\n**~~22SAR~~**\n\n**3 M0nth**\n**14 b00st**\n**~~44SAR~~**\n\n**السعر الحالي**\n\n**1 M0nth**\n**14 b00st**\n**14SAR**\n\n**3 M0nth**\n**14 b00st**\n**22SAR**\n\n\n||@here @everyone||"
    embed = discord.Embed(title="🎁 البوستات", description="اضغط الزر بالأسفل للتفاصيل", color=0x5c3a75)
    embed.set_image(url=IMAGE_URL)
    await interaction.response.send_message("تم الإرسال", ephemeral=True)
    await interaction.channel.send(embed=embed, view=StoreView(text, "boost_btn_id"))

@bot.tree.command(name="send_nitro", description="إرسال متجر النيترو")
async def send_nitro(interaction: discord.Interaction):
    text = "# **تم تـ9فير نيتر9 Gift**\n\n**Nitr0 M0nth**\n**12SAR**\n\n||@here @everyone||"
    embed = discord.Embed(title="🎁 نيترو Droy Store", description="اضغط الزر بالأسفل للتفاصيل", color=0x5c3a75)
    embed.set_image(url=IMAGE_URL)
    await interaction.response.send_message("تم الإرسال", ephemeral=True)
    await interaction.channel.send(embed=embed, view=StoreView(text, "nitro_btn_id"))

# أمر المزامنة (لحذف التكرار - استخدمه مرة واحدة فقط!)
@bot.command()
async def sync(ctx):
    guild = discord.Object(id=MY_GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    synced = await bot.tree.sync(guild=guild)
    await ctx.send(f"✅ تم مزامنة {len(synced)} أمر بنجاح!")

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    if TARGET_CHANNEL_ID != 0 and message.channel.id == TARGET_CHANNEL_ID:
        embed = discord.Embed(color=0x808080)
        embed.set_image(url=IMAGE_URL)
        await message.channel.send(embed=embed)
    await bot.process_commands(message)

@bot.event
async def on_ready():
    bot.add_view(FeedbackView())
    bot.add_view(StoreView("", "boost_btn_id"))
    bot.add_view(StoreView("", "nitro_btn_id"))
    print(f'✅ البوت يعمل الآن: {bot.user}')
    await bot.change_presence(activity=discord.Game(name="SL6E"))

TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(TOKEN)
