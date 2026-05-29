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
# (نفس الكود السابق للتقييم، تم اختصاره هنا للمساحة)
class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="اضغط هنا للتقييم", style=discord.ButtonStyle.green, emoji="📝", custom_id="review_btn")
    async def open_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        # هنا يتم استدعاء FeedbackModal
        pass 

# --- 2. نظام المتجر ---
class StoreView(View):
    def __init__(self, details, c_id):
        super().__init__(timeout=None)
        self.details = details
        self.show_details.custom_id = c_id
    @discord.ui.button(label="عرض التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
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

# --- 4. الأوامر الجديدة ---
@bot.tree.command(name="send_ticket", description="إرسال لوحة نظام التذاكر")
async def send_ticket(interaction: discord.Interaction):
    embed = discord.Embed(title="🎟️ نظام التذاكر", description="اضغط على القائمة أدناه لفتح تذكرة جديدة.", color=0x00ff00)
    await interaction.channel.send(embed=embed, view=TicketView())
    await interaction.response.send_message("✅ تم إرسال لوحة التذاكر.", ephemeral=True)

@bot.tree.command(name="send_review")
async def send_review(interaction: discord.Interaction):
    await interaction.channel.send(view=FeedbackView())
    await interaction.response.send_message("✅ تم.", ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(FeedbackView())
    bot.add_view(StoreView("", "boost_btn"))
    bot.add_view(StoreView("", "nitro_btn"))
    bot.add_view(CloseButton())
    bot.add_view(TicketView())
    await bot.tree.sync()
    print(f'✅ البوت يعمل كـ {bot.user}')

bot.run(os.environ.get('DISCORD_TOKEN'))
