import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
allowed_mentions = discord.AllowedMentions(everyone=True, roles=True, users=True)
bot = commands.Bot(command_prefix="!", intents=intents, allowed_mentions=allowed_mentions)

# ==========================================
# ⚙️ الإعدادات
# ==========================================
TARGET_CHANNEL_ID = 0  # ضع آيدي القناة هنا
SEPARATOR_IMAGE_URL = "https://media.discordapp.net/attachments/1233857597143121920/1245084930121760818/image_2.png"

# ==========================================
# ⭐ نظام التقييم
# ==========================================
class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="تقديم تقييم للمتجر")
        self.stars_input = TextInput(label="عدد النجوم (1-5)", placeholder="رقم من 1 إلى 5", min_length=1, max_length=1, required=True)
        self.add_item(self.stars_input)
        self.comment_input = TextInput(label="اكتب تقييمك", style=discord.TextStyle.paragraph, min_length=3, max_length=500, required=True)
        self.add_item(self.comment_input)

    async def on_submit(self, interaction: discord.Interaction):
        stars_text = self.stars_input.value.strip()
        if not stars_text.isdigit() or not (1 <= int(stars_text) <= 5):
            await interaction.response.send_message("❌ يجب كتابة رقم من 1 إلى 5 فقط!", ephemeral=True)
            return

        stars_emojis = "⭐" * int(stars_text)
        content = f"• {self.comment_input.value}"
        description_text = "```\n" + content + "\n```"
        
        embed = discord.Embed(
            title="✨ شكراً على تقييمك!",
            description=description_text,
            color=0x5c3a75
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="⭐ التقييم:", value=stars_emojis, inline=True)
        embed.set_footer(text="Droy Store - نظام التقييمات")
        
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("✅ تم إرسال تقييمك بنجاح!", ephemeral=True)

class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="اضغط هنا للتقييم", style=discord.ButtonStyle.green, emoji="📝")
    async def open_feedback_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal())

@bot.command()
async def send_review(ctx):
    embed = discord.Embed(title="⭐ نظام تقييمات Droy Store", description="اضغط على الزر بالأسفل لتقديم تقييمك.", color=0x5c3a75)
    await ctx.send(embed=embed, view=FeedbackView())

# ==========================================
# 🚀 متجر البوستات والنيترو
# ==========================================
class ShopView(View):
    def __init__(self, details_text):
        super().__init__(timeout=None)
        self.details_text = details_text
    
    @discord.ui.button(label="عرض التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.details_text, ephemeral=True)

@bot.command()
async def send_shop(ctx):
    text = "# **تم توفير بوستات**\n**1 Month: 14SAR**\n**3 Month: 22SAR**\n||@everyone||"
    await ctx.send(embed=discord.Embed(title="البوستات", color=0xf1c40f), view=ShopView(text))

@bot.command()
async def send_nitro(ctx):
    text = "# **تم توفير نيترو Gift**\n**Nitro Month: 12SAR**\n||@everyone||"
    await ctx.send(embed=discord.Embed(title="🎁 نيترو", color=0xf1c40f), view=ShopView(text))

# ==========================================
# 🖼️ الفاصل التلقائي
# ==========================================
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if TARGET_CHANNEL_ID != 0 and message.channel.id == TARGET_CHANNEL_ID:
        if not message.content.startswith("!"):
            embed = discord.Embed(color=message.author.color)
            embed.set_image(url=SEPARATOR_IMAGE_URL)
            await message.channel.send(embed=embed)

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'✅ البوت يعمل: {bot.user}')
    await bot.change_presence(activity=discord.Game(name="🚀"))

token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
