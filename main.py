import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput
import os
import io
import base64

GUILD_ID       = 1510735912185630812
REVIEW_CHANNEL = 1508308686932803715
GUILD_OBJ      = discord.Object(id=GUILD_ID)

intents = discord.Intents.default()
intents.message_content = True

class DroyBot(commands.Bot):
    async def setup_hook(self):
        try:
            # مزامنة أوامر السيرفر (الأسرع)
            self.tree.clear_commands(guild=GUILD_OBJ)
            synced = await self.tree.sync(guild=GUILD_OBJ)
            print(f"✅ Guild sync done: {len(synced)}")
            print("Commands:", [c.name for c in synced])

        except discord.Forbidden as e:
            # لا يطفّي البوت - fallback
            print("❌ Guild sync failed: Missing Access")
            print(f"Details: {e}")
            print("⚠️ Trying global sync fallback...")
            synced = await self.tree.sync()
            print(f"✅ Global sync done: {len(synced)}")
            print("Commands:", [c.name for c in synced])

        except Exception as e:
            print(f"❌ Unexpected sync error: {e}")
            # خله يكمل تشغيل بدل الكراش

bot = DroyBot(command_prefix="/", intents=intents)

# ======= ضع BANNER_B64 الخاص بك هنا =======
BANNER_B64 = (
    "PUT_YOUR_FULL_B64_HERE"
)
# ===========================================

def get_banner_file():
    data = base64.b64decode(BANNER_B64)
    return discord.File(io.BytesIO(data), filename="droy_banner.webp")

async def send_embed_with_banner(channel, embed, view=None):
    file = get_banner_file()
    embed.set_image(url="attachment://droy_banner.webp")
    if view:
        await channel.send(file=file, embed=embed, view=view)
    else:
        await channel.send(file=file, embed=embed)

class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="تقديم تقييم للمتجر")
        self.stars_input   = TextInput(label="عدد النجوم (1-5)", placeholder="رقم من 1 إلى 5", min_length=1, max_length=1, required=True)
        self.product_input = TextInput(label="ما هو المنتج الذي اشتريته؟", placeholder="اكتب اسم المنتج هنا...", required=True)
        self.comment_input = TextInput(label="اكتب تقييمك هنا", style=discord.TextStyle.paragraph, required=True)
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
EMOJI_COIN   = "<:droyy:1509400140362809374>"

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

# خليه global حتى يشتغل حتى لو guild access فيه مشكلة
@bot.tree.command(name="send_review", description="إرسال رسالة التقييم")
async def send_review(interaction: discord.Interaction):
    await interaction.response.send_message("جارٍ الإرسال...", ephemeral=True)
    embed = discord.Embed(title="⭐ نظام تقييمات Droy Store", description="عزيزي العميل، يسعدنا سماع رأيك!", color=0x808080)
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

@bot.tree.command(name="send_effects", description="إرسال قسم الافكتات")
async def send_effects(interaction: discord.Interaction):
    await interaction.response.send_message("جارٍ الإرسال...", ephemeral=True)
    embed = discord.Embed(title="✨ الافكتات", description="اضغط الزر بالأسفل لعرض جميع الباقات والأسعار", color=0x808080)
    await send_embed_with_banner(interaction.channel, embed, view=EffectsView())

@bot.event
async def on_ready():
    bot.add_view(FeedbackView())
    bot.add_view(StoreView("", "boost_btn"))
    bot.add_view(StoreView("", "nitro_btn"))
    bot.add_view(EffectsView())
    print(f"✅ البوت يعمل: {bot.user} | guilds={len(bot.guilds)}")

TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ DISCORD_TOKEN غير موجود.")
