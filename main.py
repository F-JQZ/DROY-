import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput
import os
import io
import base64

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# صورة Droy Store مدمجة مباشرة في الكود
BANNER_B64 = (
    "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"
    "UM0UJJmJDkpxm1PTy4YiX/uAAA="
)

def get_banner_file():
    data = base64.b64decode(BANNER_B64)
    return discord.File(io.BytesIO(data), filename="droy_banner.webp")

# دالة مساعدة لإرسال embed مع صورة البانر
async def send_embed_with_banner(channel, embed, view=None):
    file = get_banner_file()
    embed.set_image(url="attachment://droy_banner.webp")
    if view:
        await channel.send(file=file, embed=embed, view=view)
    else:
        await channel.send(file=file, embed=embed)

# ==========================================
# ⭐ نظام التقييم
# ==========================================
class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="تقديم تقييم للمتجر")

        self.stars_input = TextInput(
            label="عدد النجوم (1-5)",
            placeholder="رقم من 1 إلى 5",
            min_length=1,
            max_length=1,
            required=True
        )
        self.add_item(self.stars_input)

        self.product_input = TextInput(
            label="ما هو المنتج الذي اشتريته؟",
            placeholder="اكتب اسم المنتج هنا...",
            required=True
        )
        self.add_item(self.product_input)

        self.comment_input = TextInput(
            label="اكتب تقييمك هنا",
            style=discord.TextStyle.paragraph,
            required=True
        )
        self.add_item(self.comment_input)

    async def on_submit(self, interaction: discord.Interaction):
        stars_text = self.stars_input.value.strip()

        if not stars_text.isdigit() or not (1 <= int(stars_text) <= 5):
            await interaction.response.send_message(
                "❌ خطأ: يجب كتابة رقم من 1 إلى 5 في خانة النجوم!",
                ephemeral=True
            )
            return

        stars_number = int(stars_text)
        stars_emojis = "⭐" * stars_number

        embed = discord.Embed(
            title="✨ شكراً على تقييمك !",
            description=f"```\n• {self.comment_input.value}\n```",
            color=0x808080
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url
        )
        embed.add_field(name="⭐ تقييم الخدمة :", value=stars_emojis, inline=False)
        embed.add_field(name="📦 المنتج :", value=self.product_input.value, inline=False)
        embed.set_footer(text="Droy Store - نظام التقييمات")

        channel = interaction.client.get_channel(1508308686932803715)

        if channel:
            await channel.send(embed=embed)
            await interaction.response.send_message(
                "✅ تم إرسال تقييمك بنجاح للروم المخصص!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ خطأ: لم يتم العثور على الروم المخصص لإرسال التقييم!",
                ephemeral=True
            )


class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="اضغط هنا للتقييم",
        style=discord.ButtonStyle.green,
        emoji="📝",
        custom_id="review_btn"
    )
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

    @discord.ui.button(
        label="عرض جميع التفاصيل",
        style=discord.ButtonStyle.blurple,
        emoji="🛒"
    )
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.details, ephemeral=True)


# ==========================================
# 📨 الأوامر
# ==========================================
@bot.tree.command(name="send_review", description="إرسال رسالة التقييم")
async def send_review(interaction: discord.Interaction):
    await interaction.response.send_message("جارٍ الإرسال...", ephemeral=True)
    embed = discord.Embed(
        title="⭐ نظام تقييمات Droy Store",
        description="عزيزي العميل، يسعدنا سماع رأيك في خدماتنا!",
        color=0x808080
    )
    await send_embed_with_banner(interaction.channel, embed, view=FeedbackView())


@bot.tree.command(name="send_shop", description="إرسال متجر البوستات")
async def send_shop(interaction: discord.Interaction):
    await interaction.response.send_message("جارٍ الإرسال...", ephemeral=True)
    text = (
        "# **تم تـ9فير بـ0ستات**\n"
        "1 Month - 12 SAR\n"
        "3 Month - 17 SAR\n"
        "||@here @everyone||"
    )
    embed = discord.Embed(
        title="🚀 البوستات",
        description="اضغط الزر بالأسفل للتفاصيل",
        color=0x808080
    )
    await send_embed_with_banner(interaction.channel, embed, view=StoreView(text, "boost_btn"))


@bot.tree.command(name="send_nitro", description="إرسال متجر النيترو")
async def send_nitro(interaction: discord.Interaction):
    await interaction.response.send_message("جارٍ الإرسال...", ephemeral=True)
    text = (
        "# **تم تـ9فير نيتر9 Gift**\n"
        "Nitro Month - 14 SAR\n"
        "||@here @everyone||"
    )
    embed = discord.Embed(
        title="🎁 نيترو",
        description="اضغط الزر بالأسفل للتفاصيل",
        color=0x808080
    )
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
