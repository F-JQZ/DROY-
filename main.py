import os
import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput
from discord import app_commands # تم إضافة هذا السطر
import asyncio

intents = discord.Intents.default()
intents.message_content = True
allowed_mentions = discord.AllowedMentions(everyone=True, roles=True, users=True)
bot = commands.Bot(command_prefix="!", intents=intents, allowed_mentions=allowed_mentions)

# ==========================================
# ⚙️ الإعدادات — عدّلها حسب حاجتك
# ==========================================
TARGET_CHANNEL_ID = 0  
SEPARATOR_IMAGE_URL = "https://media.discordapp.net/attachments/1233857597143121920/1245084930121760818/image_2.png"



# ==========================================
# 🎫 نظام التيكت (Ticket System)
# ==========================================

# --- ضع هذه الآيديات في بداية ملف البوت ---
STAFF_ROLE_ID = 000000000000000000
OPEN_TICKETS_CATEGORY_ID = 000000000000000000
CLOSED_TICKETS_CATEGORY_ID = 000000000000000000

class TicketControlView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.secondary, emoji="🔒", custom_id="close_ticket_btn")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        channel = interaction.channel
        guild = interaction.guild
        closed_category = guild.get_channel(CLOSED_TICKETS_CATEGORY_ID)
        staff_role = guild.get_role(STAFF_ROLE_ID)
        
        new_name = f"🔒-{channel.name}"
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        await channel.edit(name=new_name, category=closed_category, overwrites=overwrites)
        await channel.send("🔒 **تم إغلاق التذكرة بنجاح.**")

class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="شراء منتجات المتجر", emoji="🛒", value="buy"),
            discord.SelectOption(label="استفسار", emoji="❓", value="info")
        ]
        super().__init__(placeholder="اضغط هنا لفتح تذكرة...", min_values=1, max_values=1, custom_id="ticket_select_menu")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        staff_role = guild.get_role(STAFF_ROLE_ID)
        open_category = guild.get_channel(OPEN_TICKETS_CATEGORY_ID)
        ticket_number = f"{random.randint(1, 9999):04d}"
        
        channel_name = f"{'شراء' if self.values[0] == 'buy' else 'استفسار'}-{ticket_number}"
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        ticket_channel = await guild.create_text_channel(name=channel_name, category=open_category, overwrites=overwrites)
        await interaction.response.send_message(f"✅ تم فتح التذكرة: {ticket_channel.mention}", ephemeral=True)
        
        embed = discord.Embed(title="تذكرة جديدة", description=f"أهلاً {user.mention}، سيتم الرد عليك قريباً.", color=0x7f8c8d)
        await ticket_channel.send(content=f"{user.mention} {staff_role.mention}", embed=embed, view=TicketControlView())

class TicketDropdownView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

# هذا هو الكوماند الذي يرسل البنل
@bot.tree.command(name="send_ticket", description="إرسال قائمة التذاكر")
@app_commands.checks.has_permissions(administrator=True)
async def send_ticket(interaction: discord.Interaction):
    embed = discord.Embed(title="🎫 مركز الدعم الفني", description="اختر نوع التذكرة من القائمة:", color=0x7f8c8d)
    await interaction.response.send_message("✅ تم الإرسال", ephemeral=True)
    await interaction.channel.send(embed=embed, view=TicketDropdownView())

# ==========================================
# ⭐ نظام التقييم — Droy Store (نفس كودك)
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
            await interaction.response.send_message("❌ خطأ: يجب أن تكتب رقماً من 1 إلى 5 فقط!", ephemeral=True)
            return
        stars_number = int(stars_text)
        stars_emojis = "⭐" * stars_number
        embed = discord.Embed(title="✨ شكراً على تقييمك!", description=f"\n```\n• {comment}\n```", color=0x5c3a75)
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

# ==========================================
# 🚀 متجر البوستات والنيترو (نفس كودك)
# ==========================================

class BoostView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        details_text = ("# **تم تـ9فير بـ0ستات**\n\n**1 M0nth**\n**14 b00st**\n**~~22SAR~~**\n\n**3 M0nth**\n**14 b00st**\n**~~44SAR~~**\n\n**السعر الحالي**\n\n**1 M0nth**\n**14 b00st**\n**14SAR**\n\n**3 M0nth**\n**14 b00st**\n**22SAR**\n\n\n||@here @everyone||")
        await interaction.response.send_message(details_text, ephemeral=True)

class NitroView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        details_text = ("# **تم تـ9فير نيتر9 Gift**\n\n**Nitr0 M0nth**\n**12SAR**\n\n||@here @everyone||")
        await interaction.response.send_message(details_text, ephemeral=True)

# ==========================================
# 📋 الأوامر (تم تحويلها لـ Slash Commands)
# ==========================================

@bot.tree.command(name="send_review", description="يرسل رسالة التقييم")
async def send_review(interaction: discord.Interaction):
    embed = discord.Embed(title="⭐ نظام تقييمات Droy Store", description="اضغط الزر بالأسفل لتقديم تقييمك.", color=0x5c3a75)
    await interaction.response.send_message(embed=embed, view=FeedbackView())

@bot.tree.command(name="send_shop", description="يرسل متجر البوستات")
async def send_shop(interaction: discord.Interaction):
    embed = discord.Embed(title="اـوىىىـتات 🎁 د", description="اضغط الزر بالأسفل لكامل التفاصيل", color=0xf1c40f)
    embed.set_image(url=SEPARATOR_IMAGE_URL)
    await interaction.response.send_message(embed=embed, view=BoostView())

@bot.tree.command(name="send_nitro", description="يرسل متجر النيترو")
async def send_nitro(interaction: discord.Interaction):
    embed = discord.Embed(title="🎁 ـنيـتـ،ـرو", description="اضغط الزر بالأسفل لكامل التفاصيل", color=0xf1c40f)
    await interaction.response.send_message(embed=embed, view=NitroView())

# ==========================================
# 🖼️ الفاصل والتشغيل
# ==========================================

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    if TARGET_CHANNEL_ID != 0 and message.channel.id == TARGET_CHANNEL_ID:
        embed = discord.Embed(color=message.author.color)
        embed.set_image(url=SEPARATOR_IMAGE_URL)
        await message.channel.send(embed=embed)
    await bot.process_commands(message)

@bot.event
async def on_ready():
    await bot.tree.sync() # هذا السطر ضروري جداً لظهور الكوماندات في الديسكورد
    print(f'✅ تم تشغيل البوت بنجاح باسم: {bot.user}')
    await bot.change_presence(activity=discord.Game(name="Droy
    sl6e"))

TOKEN = os.environ.get('DISCORD_TOKEN')
if __name__ == "__main__":
    bot.run(TOKEN)
