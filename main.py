import discord
from discord import app_commands  
from discord.ext import commands
from discord.ui import View, Modal, TextInput, Select
import asyncio
import os
import random

# تفعيل الـ Intents بالكامل لقراءة الرسائل والأعضاء وتجنب الكراش
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True 
allowed_mentions = discord.AllowedMentions(everyone=True, roles=True, users=True)

# إعداد البوت ليدعم السلاش كوماندز رسميًا
bot = commands.Bot(command_prefix="/", intents=intents, allowed_mentions=allowed_mentions)

# ==========================================
# ⚙️ الإعدادات — آيديهات سيرفرك
# ==========================================

MY_GUILD_ID = 1502777009087185056  # آيدي السيرفر الخاص بك للمزامنة الفورية
TARGET_CHANNEL_ID = 1508308686932803715 
SEPARATOR_IMAGE_URL = "https://media.discordapp.net/attachments/1233857597143121920/1245091722830811218/cdf7074f1d9df649.png"

# ==========================================
# ⭐ نظام التقييم — Droy Store
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

        if not stars_text.isdigit() or not (1 <= int(stars_text) <= 5):
            await interaction.response.send_message("❌ خطأ: يجب أن تكتب رقماً من 1 إلى 5 فقط في خانة النجوم!", ephemeral=True)
            return

        stars_number = int(stars_text)
        stars_emojis = "⭐" * stars_number

        embed = discord.Embed(
            title="✨ شكراً على تقييمك!",
            description=f"""\n```\n• {comment}\n
```""",
            color=0x808080
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="⭐ تقييم الخدمة :", value=stars_emojis, inline=True)
        embed.add_field(name="📦 المنتج :", value="خدمة / منتج من المتجر", inline=True)
        embed.set_footer(text="Droy Store - نظام التقييمات")

        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("✅ تم إرسال تقييمك بنجاح، شكراً لك!", ephemeral=True)


class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="اضغط هنا للتقييم", style=discord.ButtonStyle.green, emoji="📝")
    async def open_feedback_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal())


# أمر إرسال التقييم بالسلاش كوماند
@bot.tree.command(name="send_review", description="يرسل رسالة التقييم الثابتة مع الزر")
async def send_review(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⭐ نظام تقييمات Droy Store",
        description="عزيزي العميل، يسعدنا سماع رأيك في خدماتنا!\n\nاضغط على الزر بالأسفل لتقديم تقييمك بخصوص الخدمة.",
        color=0x5c3a75
    )
    await interaction.response.send_message("✅ تم إرسال بنل التقييم بنجاح!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=FeedbackView())

# ==========================================
# 🚀 متجر البوستات
# ==========================================

class BoostView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        details_text = (
            "# **تم تـ9فير بـ0ستات**\n\n"
            "**1 M0nth**\n"
            "**14 b00st**\n"
            "**~~22SAR~~**\n\n"
            "**3 M0nth**\n"
            "**14 b00st**\n"
            "**~~44SAR~~**\n\n"
            "**السعر الحالي**\n\n"
            "**1 M0nth**\n"
            "**14 b00st**\n"
            "**14SAR**\n\n"
            "**3 M0nth**\n"
            "**14 b00st**\n"
            "**22SAR**\n\n\n"
            "||@here @everyone||"
        )
        await interaction.response.send_message(details_text, ephemeral=True)


# أمر متجر البوستات بالسلاش كوماند
@bot.tree.command(name="send_shop", description="يرسل متجر البوستات")
async def send_shop(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎁 البوستات",
        description="اضغط على زر ( عرض جميع التفاصيل )\n\nاضغط الزر بالأسفل لكامل التفاصيل",
        color=0x808080
    )
    embed.set_image(url=SEPARATOR_IMAGE_URL)
    await interaction.response.send_message("✅ تم إرسال متجر البوستات بنجاح!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=BoostView())

# ==========================================
# 🎁 متجر النيترو
# ==========================================

class NitroView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        details_text = (
            "# **تم تـ9فير نيتر9 Gift**\n\n"
            "**Nitr0 M0nth**\n"
            "**12SAR**\n\n"
            "||@here @everyone||"
        )
        await interaction.response.send_message(details_text, ephemeral=True)


# أمر متجر النيترو بالسلاش كوماند
@bot.tree.command(name="send_nitro", description="يرسل متجر النيترو")
async def send_nitro(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎁 نيترو",
        description="اضغط على زر ( عرض جميع التفاصيل )\n\nاضغط الزر بالأسفل لكامل التفاصيل",
        color=0x808080
    )
    await interaction.response.send_message("✅ تم إرسال متجر النيترو بنجاح!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=NitroView())

# ==========================================
# 🖼️ الفاصل التلقائي بعد كل رسالة
# ==========================================

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if TARGET_CHANNEL_ID != 0 and message.channel.id == TARGET_CHANNEL_ID:
        embed = discord.Embed(color=message.author.color)
        embed.set_image(url=SEPARATOR_IMAGE_URL)
        await message.channel.send(embed=embed)

    await bot.process_commands(message)

# ==========================================
# ✅ تشغيل البوت والمزامنة الفورية في سيرفرك
# ==========================================

@bot.event
async def on_ready():
    # تسجيل الفيو الثابتة حتى لا تتعطل عند إعادة تشغيل البوت
    bot.add_view(FeedbackView())
    bot.add_view(BoostView())
    bot.add_view(NitroView())
    bot.add_view(TicketDropdownView())
    bot.add_view(TicketControlView())
    
    # دالة لمزامنة السلاش كوماندز تلقائيًا وفوريًا داخل سيرفرك المحدد
    try:
        guild = discord.Object(id=MY_GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        print(f"⚙️ تم مزامنة {len(synced)} من الأوامر المائلة في سيرفرك بنجاح وبشكل فوري!")
    except Exception as e:
        print(f"❌ فشل مزامنة الأوامر: {e}")
        
    print(f'✅ تم تشغيل البوت بنجاح باسم: {bot.user}')
    
    # تظهر حالة البوت باسم droy بشكل رسمي وثابت
    await bot.change_presence(activity=discord.Game(name="droy 🚀"))

# قراءة التوكن من لوحة تحكم Railway أو الاستضافة بأمان
TOKEN = os.environ.get('DISCORD_TOKEN')
if __name__ == "__main__":
    bot.run(TOKEN)
