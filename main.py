import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput
import os
import io
import base64
import binascii

GUILD_ID = 1510735912185630812
REVIEW_CHANNEL = 1508308686932803715

# هذه IDs للإيموجيات الخاصة
BOOST_EMOJI_ID = 1507172355997433887
NITRO_EMOJI_ID = 1507172336292466789

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
    "PUT_YOUR_FULL_B64_HERE_EXACTLY_AS_IS"
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


def emoji_or_fallback(bot_client: commands.Bot, emoji_id: int, fallback: str) -> str:
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

EFFECTS_DETAILS = (
    "# ✨ باقات الافكتات\n\n"
    f"{EMOJI_DOLLAR} **4.99$** ➜ **9** {EMOJI_COIN}\n"
    f"{EMOJI_DOLLAR} **5.99$** ➜ **10.5** {EMOJI_COIN}\n"
    f"{EMOJI_DOLLAR} **6.99$** ➜ **12** {EMOJI_COIN}\n"
    f"{EMOJI_DOLLAR} **7.99$** ➜ **13** {EMOJI_COIN}\n"
    f"{EMOJI_DOLLAR} **9.99$** ➜ **18** {EMOJI_COIN}\n"
    f"{EMOJI_DOLLAR} **11.99$** ➜ **19.5** {EMOJI_COIN}\n"
)


class EffectsView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="✨", custom_id="effects_btn")
    async def show_effects(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(EFFECTS_DETAILS, ephemeral=True)


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

    shop_icon = emoji_or_fallback(interaction.client, BOOST_EMOJI_ID, "🚀")

    text = (
        "# **تم تـ9فير بـ0ستات**\n"
        f"1 Month - 12 {EMOJI_COIN}\n"
        f"3 Month - 17 {EMOJI_COIN}\n"
        "||@here @everyone||"
    )
    embed = discord.Embed(
        title=f"{shop_icon} البوستات",
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
        title=f"{nitro_icon} نيترو",
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


@bot.event
async def on_ready():
    bot.add_view(FeedbackView())
    bot.add_view(StoreView("", "boost_btn"))
    bot.add_view(StoreView("", "nitro_btn"))
    bot.add_view(EffectsView())
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
