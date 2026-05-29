import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput, Select
import asyncio
import os
import random

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
allowed_mentions = discord.AllowedMentions(everyone=True, roles=True, users=True)

bot = commands.Bot(command_prefix="!", intents=intents, allowed_mentions=allowed_mentions)

# ==========================================
# ⚙️ الإعدادات
# ==========================================
TARGET_CHANNEL_ID = 1508308686932803715 
SEPARATOR_IMAGE_URL = "https://media.discordapp.net/attachments/1233857597143121920/1245091722830811218/cdf7074f1d9df649.png"
OPEN_TICKETS_CATEGORY_ID = 123456789012345678    
CLOSED_TICKETS_CATEGORY_ID = 876543210987654321 
STAFF_ROLE_ID = 112233445566778899 

# ==========================================
# 🎫 نظام التيكت
# ==========================================

class TicketControlView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.secondary, emoji="🔒", custom_id="persistent_close_ticket_btn")
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
        await channel.send(embed=discord.Embed(description="🔒 **تم إغلاق التذكرة بنجاح.**", color=0x7f8c8d))

class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="شراء منتجات المتجر", emoji="🛒", value="buy"),
            discord.SelectOption(label="استفسار", emoji="❓", value="info")
        ]
        super().__init__(placeholder="اضختار نوع التذكرة...", options=options, custom_id="persistent_ticket_select")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        staff_role = guild.get_role(STAFF_ROLE_ID)
        open_category = guild.get_channel(OPEN_TICKETS_CATEGORY_ID)
        ticket_num = f"{random.randint(1, 9999):04d}"
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await guild.create_text_channel(name=f"{self.values[0]}-{ticket_num}", category=open_category, overwrites=overwrites)
        await interaction.response.send_message(f"✅ تم فتح التذكرة: {channel.mention}", ephemeral=True)
        await channel.send(content=f"{user.mention}", embed=discord.Embed(title="تذكرة جديدة", color=0x7f8c8d), view=TicketControlView())

class TicketDropdownView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

# ==========================================
# ⭐ التقييم
# ==========================================

class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="تقديم تقييم")
        self.stars = TextInput(label="النجوم (1-5)", min_length=1, max_length=1)
        self.comment = TextInput(label="رأيك", style=discord.TextStyle.paragraph)
        self.add_item(self.stars)
        self.add_item(self.comment)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅ شكراً لتقييمك!", ephemeral=True)
        await interaction.channel.send(embed=discord.Embed(title=f"تقييم: {'⭐'*int(self.stars.value)}", description=self.comment.value, color=0x5c3a75))

class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="اضغط هنا للتقييم", style=discord.ButtonStyle.green, custom_id="persistent_feedback_btn")
    async def open_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal())

# ==========================================
# 🚀 المتاجر (Persistent)
# ==========================================

class ShopView(View):
    def __init__(self, cid, text):
        super().__init__(timeout=None)
        self.text = text
        self.add_item(discord.ui.Button(label="عرض التفاصيل", style=discord.ButtonStyle.blurple, custom_id=cid))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        await interaction.response.send_message(self.text, ephemeral=True)
        return True

# ==========================================
# 🏁 تشغيل
# ==========================================

@bot.event
async def on_ready():
    bot.add_view(FeedbackView())
    bot.add_view(TicketDropdownView())
    bot.add_view(TicketControlView())
    bot.add_view(ShopView("p_boost_btn", "تفاصيل البوستات هنا..."))
    bot.add_view(ShopView("p_nitro_btn", "تفاصيل النيترو هنا..."))
    print(f'✅ البوت يعمل باسم: {bot.user}')
    await bot.change_presence(activity=discord.Game(name="droy 🚀"))

@bot.event
async def on_message(message):
    if message.author != bot.user and TARGET_CHANNEL_ID != 0 and message.channel.id == TARGET_CHANNEL_ID:
        await message.channel.send(embed=discord.Embed().set_image(url=SEPARATOR_IMAGE_URL))
    await bot.process_commands(message)

# أوامر الإرسال
@bot.command()
async def send_ticket(ctx): await ctx.send("مركز التيكت:", view=TicketDropdownView())
@bot.command()
async def send_review(ctx): await ctx.send("نظام التقييم:", view=FeedbackView())

bot.run(os.environ.get('DISCORD_TOKEN'))
