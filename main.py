import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput, Select
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

IMAGE_URL = "https://media.discordapp.net/attachments/1233857597143121920/1245084930121760818/image_2.png"

# --- 1. نظام التقييم ---
class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="تقديم تقييم للمتجر")
        self.stars_input = TextInput(label="عدد النجوم (1-5)", placeholder="رقم من 1 إلى 5", min_length=1, max_length=1, required=True)
        self.add_item(self.stars_input)
        self.product_input = TextInput(label="المنتج", placeholder="اكتب اسم المنتج...", required=True)
        self.add_item(self.product_input)
        self.comment_input = TextInput(label="تقييمك", style=discord.TextStyle.paragraph, required=True)
        self.add_item(self.comment_input)

    async def on_submit(self, interaction: discord.Interaction):
        stars_text = self.stars_input.value.strip()
        if not stars_text.isdigit() or not (1 <= int(stars_text) <= 5):
            await interaction.response.send_message("❌ خطأ: يجب كتابة رقم من 1 إلى 5!", ephemeral=True)
            return
        
        embed = discord.Embed(title="✨ شكراً على تقييمك!", description=f"```\n• {self.comment_input.value}\n```", color=0x808080)
        embed.add_field(name="⭐ التقييم:", value="⭐" * int(stars_text), inline=False)
        embed.add_field(name="📦 المنتج:", value=self.product_input.value, inline=False)
        
        channel = interaction.client.get_channel(1508308686932803715)
        if channel:
            await channel.send(embed=embed)
            await interaction.response.send_message("✅ تم إرسال تقييمك بنجاح!", ephemeral=True)

class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="اضغط هنا للتقييم", style=discord.ButtonStyle.green, emoji="📝", custom_id="review_btn")
    async def open_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal())

# --- 2. نظام المتجر ---
class StoreView(View):
    def __init__(self, details, c_id):
        super().__init__(timeout=None)
        self.details = details
        self.show_details.custom_id = c_id

    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.details, ephemeral=True)

# --- 3. نظام التذاكر ---
class CloseButton(View):
    def __init__(self, owner_id=None):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    @discord.ui.button(label="إغلاق التذكرة", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        admin_role_id = 1234567890 
        if any(role.id == admin_role_id for role in interaction.user.roles) or interaction.user.id == self.owner_id:
            await interaction.response.send_message("سيتم إغلاق القناة...")
            await asyncio.sleep(3)
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("ليس لديك صلاحية!", ephemeral=True)

class TicketSelect(Select):
    def __init__(self):
        super().__init__(placeholder="أختر القائمة", options=[discord.SelectOption(label="استفسار", value="inquiry"), discord.SelectOption(label="شراء", value="purchase")])
    async def callback(self, interaction: discord.Interaction):
        channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}")
        await channel.send(f"أهلاً {interaction.user.mention}", view=CloseButton(owner_id=interaction.user.id))
        await interaction.response.send_message(f"تم فتح تذكرتك: {channel.mention}", ephemeral=True)

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

# --- 4. الأوامر ---
@bot.tree.command(name="send_review")
async def send_review(interaction: discord.Interaction):
    embed = discord.Embed(title="⭐ نظام تقييمات Droy Store", description="عزيزي العميل، يسعدنا سماع رأيك!", color=0x808080)
    embed.set_image(url=IMAGE_URL)
    await interaction.channel.send(embed=embed, view=FeedbackView())
    await interaction.response.send_message("تم الإرسال.", ephemeral=True)

@bot.tree.command(name="send_shop")
async def send_shop(interaction: discord.Interaction):
    text = ("# **تم توفير بوستات**\n1 Month - 14SAR\n3 Month - 22SAR\n||@here @everyone||")
    embed = discord.Embed(title="🎁 البوستات", description="اضغط الزر بالأسفل للتفاصيل", color=0x808080)
    embed.set_image(url=IMAGE_URL)
    await interaction.channel.send(embed=embed, view=StoreView(text, "boost_btn"))
    await interaction.response.send_message("تم الإرسال.", ephemeral=True)

@bot.tree.command(name="send_nitro")
async def send_nitro(interaction: discord.Interaction):
    text = ("# **تم توفير نيترو Gift**\nNitro Month - 12SAR\n||@here @everyone||")
    embed = discord.Embed(title="🎁 نيترو", description="اضغط الزر بالأسفل للتفاصيل", color=0x808080)
    embed.set_image(url=IMAGE_URL)
    await interaction.channel.send(embed=embed, view=StoreView(text, "nitro_btn"))
    await interaction.response.send_message("تم الإرسال.", ephemeral=True)

@bot.event
async def on_ready():
    # تسجيل الـ Views
    bot.add_view(FeedbackView())
    bot.add_view(StoreView("", "boost_btn"))
    bot.add_view(StoreView("", "nitro_btn"))
    bot.add_view(CloseButton())
    bot.add_view(TicketView())
    await bot.tree.sync()
    print(f'✅ البوت يعمل كـ {bot.user}')

bot.run(os.environ.get('DISCORD_TOKEN'))
