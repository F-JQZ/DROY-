import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# مسار صورة Droy Store (نفس مجلد bot.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BANNER_PATH = os.path.join(BASE_DIR, "droy_banner.webp")

# دالة مساعدة لإرسال embed مع صورة البانر
async def send_embed_with_banner(channel, embed, view=None):
    if os.path.exists(BANNER_PATH):
        file = discord.File(BANNER_PATH, filename="droy_banner.webp")
        embed.set_image(url="attachment://droy_banner.webp")
        if view:
            await channel.send(file=file, embed=embed, view=view)
        else:
            await channel.send(file=file, embed=embed)
    else:
        if view:
            await channel.send(embed=embed, view=view)
        else:
            await channel.send(embed=embed)

# ==========================================
# ⭐ نظام التقييم
# ==========================================
class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="تقديم تقييم للمتجر")
        self.stars_input = TextInput(label="عدد النجوم (1-5)", placeholder="رقم من 1 إلى 5", min_length=1, max_length=1, required=True)
        self.add_item(self.stars_input)
        self.product_input = TextInput(label="ما هو المنتج الذي اشتريته؟", placeholder="اكتب اسم المنتج هنا...", required=True)
        self.add_item(self.product_input)
        self.comment_input = TextInput(label="اكتب تقييمك هنا", style=discord.TextStyle.paragraph, required=True)
        self.add_item(self.comment_input)

    async def on_submit(self, interaction: discord.Interaction):
        stars_text = self.stars_input.value.strip()
        if not stars_text.isdigit() or not (1 <= int(stars_text) <= 5):
            await interaction.response.send_message("❌ خطأ: يجب كتابة رقم من 1 إلى 5 في خانة النجوم!", ephemeral=True)
            return

        stars_number = int(stars_text)
        stars_emojis = "⭐" * stars_number

        embed = discord.Embed(title="✨ شكراً على تقييمك !", description=f"```\n• {self.comment_input.value}\n```", color=0x808080)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="⭐ تقييم الخدمة :", value=stars_emojis, inline=False)
        embed.add_field(name="📦 المنتج :", value=self.product_input.value, inline=False)
        embed.set_footer(text="Droy Store - نظام التقييمات")

        channel = interaction.client.get_channel(1508308686932803715)
        if channel:
            await channel.send(embed=embed)
            await interaction.response.send_message("✅ تم إرسال تقييمك بنجاح!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ خطأ: لم يتم العثور على الروم!", ephemeral=True)


class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="اضغط هنا للتقييم", style=discord.ButtonStyle.green, emoji="📝", custom_id="review_btn")
    async def open_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal())


# ==========================================
# 🛒 نظام المتجر
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
# 📨 الأوامر
# ==========================================
@bot.tree.command(name="send_review", description="إرسال رسالة التقييم")
async def send_review(interaction: discord.Interaction):
    await interaction.response.send_message("جارٍ الإرسال...", ephemeral=True)
    embed = discord.Embed(title="⭐ نظام تقييمات Droy Store", description="عزيزي العميل، يسعدنا سماع رأيك في خدماتنا!", color=0x808080)
    await send_embed_with_banner(interaction.channel, embed, view=FeedbackView())


@bot.tree.command(name="send_shop", description="إرسال متجر البوستات")
async def send_shop(interaction: discord.Interaction):
    await interaction.response.send_message("جارٍ الإرسال...", ephemeral=True)
    text = "# **تم تـ9فير بـ0ستات**\n1 Month - 12 SAR\n3 Month - 17 SAR\n||@here @everyone||"
    embed = discord.Embed(title="🚀 البوستات", description="اضغط الزر بالأسفل للتفاصيل", color=0x808080)
    await send_embed_with_banner(interaction.channel, embed, view=StoreView(text, "boost_btn"))


@bot.tree.command(name="send_nitro", description="إرسال متجر النيترو")
async def send_nitro(interaction: discord.Interaction):
    await interaction.response.send_message("جارٍ الإرسال...", ephemeral=True)
    text = "# **تم تـ9فير نيتر9 Gift**\nNitro Month - 14 SAR\n||@here @everyone||"
    embed = discord.Embed(title="🎁 نيترو", description="اضغط الزر بالأسفل للتفاصيل", color=0x808080)
    await send_embed_with_banner(interaction.channel, embed, view=StoreView(text, "nitro_btn"))


# ==========================================
# ✅ تشغيل البوت
# ==========================================
@bot.event
async def on_ready():
    bot.add_view(FeedbackView())
    bot.add_view(StoreView("", "boost_btn"))
    bot.add_view(StoreView("", "nitro_btn"))
    await bot.tree.sync()
    print(f"✅ البوت يعمل: {bot.user}")


bot.run(os.environ.get("DISCORD_TOKEN"))
