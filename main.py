import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput
import os
import io
import base64
import binascii

GUILD_ID = 1510735912185630812
REVIEW_CHANNEL = 1508308686932803715

# أيقونات مخصصة (نفس IDs عندك)
BOOST_EMOJI_ID = 1507172355997433887   # بوستات
NITRO_EMOJI_ID = 1507172336292466789   # نيترو

intents = discord.Intents.default()
intents.message_content = True


class DroyBot(commands.Bot):
    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        try:
            synced = await self.tree.sync(guild=guild)
            print(f"✅ Guild sync: {len(synced)}")
            print("Guild commands:", [c.name for c in synced])
        except discord.Forbidden:
            print("⚠️ Missing Access على guild sync، سيتم استخدام global sync")
            synced = await self.tree.sync()
            print(f"✅ Global sync: {len(synced)}")
            print("Global commands:", [c.name for c in synced])
        except Exception as e:
            print(f"❌ Sync error: {e}")


bot = DroyBot(command_prefix="/", intents=intents)

# ======= حط نفس BANNER_B64 القديم كامل هنا (بدون ... ) =======
BANNER_B64 = (
    "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"
    "5Vc2EUM0UJJmJDkpxm1PTy4YiX/uAAA="
    "..."
)
# ===============================================================

BANNER_BYTES = None
if BANNER_B64 and BANNER_B64 != "PUT_YOUR_FULL_B64_HERE_EXACTLY_AS_IS":
    try:
        BANNER_BYTES = base64.b64decode(BANNER_B64, validate=False)
        print("✅ Banner loaded")
    except (binascii.Error, ValueError) as e:
        BANNER_BYTES = None
        print(f"⚠️ Banner decode error: {e}")


def get_banner_file():
    if not BANNER_BYTES:
        return None
    return discord.File(io.BytesIO(BANNER_BYTES), filename="droy_banner.webp")


def emoji_or_fallback(bot_client, emoji_id: int, fallback: str) -> str:
    """يرجع الإيموجي كصورة، مو كنص :nitro:"""
    e = bot_client.get_emoji(emoji_id)
    return str(e) if e else fallback


async def send_embed_with_banner(channel, embed, view=None):
    file = get_banner_file()
    if file:
        embed.set_image(url="attachment://droy_banner.webp")
        await channel.send(file=file, embed=embed, view=view)
    else:
        await channel.send(embed=embed, view=view)


class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="تقديم تقييم للمتجر")
        self.stars_input = TextInput(
            label="عدد النجوم (1-5)",
            placeholder="رقم من 1 إلى 5",
            min_length=1,
            max_length=1,
            required=True,
        )
        self.product_input = TextInput(
            label="ما هو المنتج الذي اشتريته؟",
            placeholder="اكتب اسم المنتج هنا...",
            required=True,
        )
        self.comment_input = TextInput(
            label="اكتب تقييمك هنا",
            style=discord.TextStyle.paragraph,
            required=True,
        )
        self.add_item(self.stars_input)
        self.add_item(self.product_input)
        self.add_item(self.comment_input)

    async def on_submit(self, interaction: discord.Interaction):
        stars_text = self.stars_input.value.strip()
        if not stars_text.isdigit() or not (1 <= int(stars_text) <= 5):
            await interaction.response.send_message("❌ خطأ: يجب كتابة رقم من 1 إلى 5!", ephemeral=True)
            return

        stars_emojis = "⭐" * int(stars_text)
        embed = discord.Embed(
            title="✨ شكراً على تقييمك !",
            description=f"```\n• {self.comment_input.value}\n```",
            color=0x808080,
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="⭐ تقييم الخدمة :", value=stars_emojis, inline=False)
        embed.add_field(name="📦 المنتج :", value=self.product_input.value, inline=False)
        embed.set_footer(text="Droy Store - نظام التقييمات")

        channel = interaction.client.get_channel(REVIEW_CHANNEL)
        if channel:
            await channel.send(embed=embed)
            await interaction.response.send_message("✅ تم إرسال تقييمك!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ لم يتم العثور على الروم!", ephemeral=True)


class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="اضغط هنا للتقييم", style=discord.ButtonStyle.green, emoji="📝", custom_id="review_btn")
    async def open_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal())


class StoreView(View):
    def __init__(self, details: str, c_id: str):
        super().__init__(timeout=None)
        self.details = details
        self.show_details.custom_id = c_id

    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.details, ephemeral=True)


EMOJI_DOLLAR = "<:Droyy:1509313014564651228>"
EMOJI_COIN = "<:droyy:1509400140362809374>"
EMOJI_RYAL = "<:Dm3_Ryal:1382488114731155456>"

EFFECTS_DETAILS = (
    "# ✨ باقات الافكتات\n\n"
    f"{EMOJI_DOLLAR} **4.99$** ➜ **9** {EMOJI_COIN}\n"
    f"{EMOJI_DOLLAR} **5.99$** ➜ **10.5** {EMOJI_COIN}\n"
    f"{EMOJI_DOLLAR} **6.99$** ➜ **12** {EMOJI_COIN}\n"
    f"{EMOJI_DOLLAR} **7.99$** ➜ **13** {EMOJI_COIN}\n"
    f"{EMOJI_DOLLAR} **9.99$** ➜ **18** {EMOJI_COIN}\n"
    f"{EMOJI_DOLLAR} **11.99$** ➜ **19.5** {EMOJI_COIN}\n"
)

# تفاصيل باقات الأعضاء الجديدة
MEMBERS_DETAILS = (
    "# 👥 باقات أعضاء ديسكورد\n\n"
    "-* **اعضاء دسكورد اونلاين**\n"
    f"**500**{EMOJI_COIN} بـ **5** \n"
    f"**1000**{EMOJI_COIN} بـ **10** \n\n"
    "-* **اعضاء دسكورد اوفلاين**\n"
    f"**500** بـ **{EMOJI_COIN}2.50** \n"
    f"**1000** بـ **{EMOJI_COIN}5** \n"
)


class EffectsView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="✨", custom_id="effects_btn")
    async def show_effects(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(EFFECTS_DETAILS, ephemeral=True)


# كلاس الأزرار الخاص بقسم الأعضاء الجديد
class MembersView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="👥", custom_id="members_btn")
    async def show_members(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(MEMBERS_DETAILS, ephemeral=True)


@bot.tree.command(name="send_review", description="إرسال رسالة التقييم")
async def send_review(interaction: discord.Interaction):
    await interaction.response.send_message("✅ جاري الإرسال...", ephemeral=True)
    embed = discord.Embed(
        title="⭐ نظام تقييمات Droy Store",
        description="عزيزي العميل، يسعدنا سماع رأيك!",
        color=0x808080,
    )
    await send_embed_with_banner(interaction.channel, embed, view=FeedbackView())


@bot.tree.command(name="send_shop", description="إرسال متجر البوستات")
async def send_shop(interaction: discord.Interaction):
    await interaction.response.send_message("✅ جاري الإرسال...", ephemeral=True)

    boost_icon = emoji_or_fallback(interaction.client, BOOST_EMOJI_ID, "💎")

    text = (
        "# **تم تـ9فير بـ0ستات**\n"
        f"1 Month - 12 {EMOJI_COIN}\n"
        f"3 Month - 17 {EMOJI_COIN}\n"
        "||@here @everyone||"
    )
    embed = discord.Embed(
        title=f"البوستات {boost_icon}",
        description="اضغط الزر بالأسفل للتفاصيل",
        color=0x808080,
    )
    await send_embed_with_banner(interaction.channel, embed, view=StoreView(text, "boost_btn"))


@bot.tree.command(name="send_nitro", description="إرسال متجر النيترو")
async def send_nitro(interaction: discord.Interaction):
    await interaction.response.send_message("✅ جاري الإرسال...", ephemeral=True)

    nitro_icon = emoji_or_fallback(interaction.client, NITRO_EMOJI_ID, "🎁")

    text = (
        "# **تم تـ9فير نيتر9 Gift**\n"
        f"Nitro Month - 14 {EMOJI_COIN}\n"
        "||@here @everyone||"
    )
    embed = discord.Embed(
        title=f"نيترو {nitro_icon}",
        description="اضغط الزر بالأسفل للتفاصيل",
        color=0x808080,
    )
    await send_embed_with_banner(interaction.channel, embed, view=StoreView(text, "nitro_btn"))


@bot.tree.command(name="send_effects", description="إرسال قسم الافكتات")
async def send_effects(interaction: discord.Interaction):
    await interaction.response.send_message("✅ جاري الإرسال...", ephemeral=True)
    embed = discord.Embed(
        title="✨ الافكتات",
        description="اضغط الزر بالأسفل لعرض جميع الباقات والأسعار",
        color=0x808080,
    )
    await send_embed_with_banner(interaction.channel, embed, view=EffectsView())


# الأمر الجديد الخاص بإرسال قسم الأعضاء
@bot.tree.command(name="send_members", description="إرسال قسم أعضاء ديسكورد")
async def send_members(interaction: discord.Interaction):
    await interaction.response.send_message("✅ جاري الإرسال...", ephemeral=True)
    embed = discord.Embed(
        title="أعضاء ديسكورد👥",
        description="اضغط الزر بالأسفل لعرض باقات الأعضاء (أونلاين / أوفلاين)",
        color=0x808080,
    )
    await send_embed_with_banner(interaction.channel, embed, view=MembersView())


@bot.event
async def on_ready():
    bot.add_view(FeedbackView())
    bot.add_view(StoreView("", "boost_btn"))
    bot.add_view(StoreView("", "nitro_btn"))
    bot.add_view(EffectsView())
    bot.add_view(MembersView()) # تسجيل عرض الأعضاء الجديد هنا ليعمل بشكل دائم
    print(f"✅ البوت يعمل: {bot.user} | guilds={len(bot.guilds)}")


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    try:
        if interaction.response.is_done():
            await interaction.followup.send(f"❌ خطأ: {error}", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ خطأ: {error}", ephemeral=True)
    except Exception:
        pass
    print(f"App command error: {error}")


TOKEN = os.environ.get("DISCORD_TOKEN")
print("TOKEN FOUND:", bool(TOKEN))

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ DISCORD_TOKEN غير موجود.")
