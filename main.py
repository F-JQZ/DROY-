import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Modal, TextInput
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True 

bot = commands.Bot(command_prefix="/", intents=intents)

# الصورة المطلوبة
IMAGE_URL = "https://media.discordapp.net/attachments/1233857597143121920/1245084930121760818/image_2.png"

# ==========================================
# 1. التقييم
# ==========================================
class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="تقديم تقييم للمتجر")
        self.stars_input = TextInput(label="عدد النجوم (من 1 إلى 5)", placeholder="اكتب رقم من 1 إلى 5 فقط...", min_length=1, max_length=1)
        self.add_item(self.stars_input)
        self.comment_input = TextInput(label="اكتب تقييمك هنا", style=discord.TextStyle.paragraph)
        self.add_item(self.comment_input)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="✨ شكراً على تقييمك!", description=f"التقييم: {'⭐'*int(self.stars_input.value)}\nالرأي: {self.comment_input.value}", color=0x808080)
        embed.set_image(url=IMAGE_URL) # الصورة تظهر هنا
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("✅ تم الإرسال!", ephemeral=True)

class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="اضغط هنا للتقييم", style=discord.ButtonStyle.green, emoji="📝", custom_id="review_btn")
    async def open_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal())

# ==========================================
# 2. المتاجر (بوستات / نيترو) بنصوصك الأصلية
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
# 3. الأوامر
# ==========================================

@bot.tree.command(name="send_review", description="إرسال رسالة التقييم")
async def send_review(interaction: discord.Interaction):
    embed = discord.Embed(title="⭐ نظام تقييمات Droy Store", description="عزيزي العميل، يسعدنا سماع رأيك في خدماتنا!\n\nاضغط على الزر بالأسفل لتقديم تقييمك.", color=0x5c3a75)
    embed.set_image(url=IMAGE_URL) # الصورة تظهر هنا
    await interaction.response.send_message("تم", ephemeral=True)
    await interaction.channel.send(embed=embed, view=FeedbackView())

@bot.tree.command(name="send_shop", description="إرسال متجر البوستات")
async def send_shop(interaction: discord.Interaction):
    text = ("# **تم تـ9فير بـ0ستات**\n\n**1 M0nth**\n**14 b00st**\n**~~22SAR~~**\n\n**3 M0nth**\n**14 b00st**\n**~~44SAR~~**\n\n**السعر الحالي**\n\n**1 M0nth**\n**14 b00st**\n**14SAR**\n\n**3 M0nth**\n**14 b00st**\n**22SAR**\n\n\n||@here @everyone||")
    embed = discord.Embed(title="🎁 البوستات", description="اضغط على زر ( عرض جميع التفاصيل )\n\nاضغط الزر بالأسفل لكامل التفاصيل", color=0x808080)
    embed.set_image(url=IMAGE_URL) # الصورة تظهر هنا
    await interaction.response.send_message("تم", ephemeral=True)
    await interaction.channel.send(embed=embed, view=StoreView(text, "boost_btn"))

@bot.tree.command(name="send_nitro", description="إرسال متجر النيترو")
async def send_nitro(interaction: discord.Interaction):
    text = ("# **تم تـ9فير نيتر9 Gift**\n\n**Nitr0 M0nth**\n**12SAR**\n\n||@here @everyone||")
    embed = discord.Embed(title="🎁 نيترو", description="اضغط على زر ( عرض جميع التفاصيل )\n\nاضغط الزر بالأسفل لكامل التفاصيل", color=0x808080)
    embed.set_image(url=IMAGE_URL) # الصورة تظهر هنا
    await interaction.response.send_message("تم", ephemeral=True)
    await interaction.channel.send(embed=embed, view=StoreView(text, "nitro_btn"))

@bot.event
async def on_ready():
    # تسجيل الـ Views
    bot.add_view(FeedbackView())
    bot.add_view(StoreView("", "boost_btn"))
    bot.add_view(StoreView("", "nitro_btn"))
    
    # مزامنة الأوامر مرة واحدة لتجنب أي دبلت
    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)
    print(f'✅ تم التشغيل بنجاح: {bot.user}')

bot.run(os.environ.get('DISCORD_TOKEN'))
