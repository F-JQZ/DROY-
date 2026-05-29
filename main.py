import discord
from discord import app_commands  # مكتبة السلاش كوماندز
from discord.ext import commands
from discord.ui import View, Modal, TextInput, Select
import asyncio
import os
import random

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
allowed_mentions = discord.AllowedMentions(everyone=True, roles=True, users=True)

# تحويل البوت ليدعم السلاش كوماندز
bot = commands.Bot(command_prefix="/", intents=intents, allowed_mentions=allowed_mentions)

# ==========================================
# ⚙️ الإعدادات — عدّلها حسب حاجتك
# ==========================================

TARGET_CHANNEL_ID = 1508308686932803715 
SEPARATOR_IMAGE_URL = "https://media.discordapp.net/attachments/1233857597143121920/1245091722830811218/cdf7074f1d9df649.png"

# 🎫 إعدادات نظام التيكت (ضع الآيديهات الخاصة بسيرفرك هنا)
OPEN_TICKETS_CATEGORY_ID = 123456789012345678    
CLOSED_TICKETS_CATEGORY_ID = 876543210987654321  
STAFF_ROLE_ID = 112233445566778899               

# ==========================================
# 🎫 نظام التيكت (Ticket System)
# ==========================================

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
        
        embed_closed = discord.Embed(
            description="🔒 **تم إغلاق التذكرة بنجاح وتحويلها للأرشيف.**",
            color=0x7f8c8d
        )
        await channel.send(embed=embed_closed)


class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="شراء منتجات المتجر", description="لشراء منتجات المتجر اضغط على هذا الخيار", emoji="🛒", value="buy"),
            discord.SelectOption(label="استفسار", description="للاستفسار اضغط على هذا الخيار", emoji="❓", value="info")
        ]
        super().__init__(placeholder="اضغط هنا لاختيار نوع التذكرة...", min_values=1, max_values=1, custom_id="ticket_select_menu")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        staff_role = guild.get_role(STAFF_ROLE_ID)
        open_category = guild.get_channel(OPEN_TICKETS_CATEGORY_ID)
        
        ticket_number = f"{random.randint(1, 9999):04d}"
        
        if self.values[0] == "buy":
            channel_name = f"شراء-{ticket_number}"
            ticket_title = "تذكرة شراء منتجات"
        else:
            channel_name = f"استفسار-{ticket_number}"
            ticket_title = "تذكرة استفسار"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True)
        }

        ticket_channel = await guild.create_text_channel(name=channel_name, category=open_category, overwrites=overwrites)
        await interaction.response.send_message(f"✅ تم فتح تذكرتك بنجاح: {ticket_channel.mention}", ephemeral=True)

        embed_welcome = discord.Embed(
            title=ticket_title,
            description=f"{user.mention}\nسيتم الرد عليك في أقرب وقت ممكن من قبل الدعم الفني.",
            color=0x7f8c8d
        )
        embed_welcome.set_footer(text="Droy Store - Ticket System")

        await ticket_channel.send(
            content=f"{user.mention} {staff_role.mention if staff_role else ''}", 
            embed=embed_welcome, 
            view=TicketControlView()
        )


class TicketDropdownView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())


# أمر إرسال بنل التيكت (Slash Command)
@bot.tree.command(name="send_ticket", description="يرسل بنل التيكت القائمة المنسدلة (للإدارة فقط)")
@app_commands.checks.has_permissions(administrator=True)
async def send_ticket(interaction: discord.Interaction):
    embed_panel = discord.Embed(
        title="🎫 مركز الدعم الفني | Droy Store",
        description="أهلاً بك في مركز المساعدة الخاص بمتجرنا.\n\nالرجاء اختيار القسم المناسب من القائمة بالأسفل لفتح تذكرة جديدة.",
        color=0x7f8c8d
    )
    await interaction.response.send_message("✅ تم إرسال بنل التيكت بنجاح!", ephemeral=True)
    await interaction.channel.send(embed=embed_panel, view=TicketDropdownView())

# ==========================================
# ⭐ نظام التقييم — Droy Store
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
            await interaction.response.send_message("❌ خطأ: يجب أن تكتب رقماً من 1 إلى 5 فقط في خانة النجوم!", ephemeral=True)
            return

        stars_number = int(stars_text)
        stars_emojis = "⭐" * stars_number

        # هنا تم تعديل وإصلاح علامات التنصيص الثلاثية المقفلة بشكل صحيح
        embed = discord.Embed(
            title="✨ شكراً على تقييمك!",
            description=f"""\n```\n• {comment}\n
```""",
            color=0x5c3a75
        )
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


# أمر إرسال التقييم (Slash Command)
@bot.tree.command(name="send_review", description="يرسل رسالة التقييم الثابتة مع الزر")
async def send_review(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⭐ نظام تقييمات Droy Store",
        description="عزيزي العميل، يسعدنا سماع رأيك في خدماتنا!\n\nاضغط على الزر بالأسفل لتقديم تقييمك بخصوص الخدمة.",
        color=0x5c3a75
    )
    await interaction.response.send_message("✅ تم إرسال بنل التقييم بنجاح!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=FeedbackView())

# ==========================================
# 🚀 متجر البوستات
# ==========================================

class BoostView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        details_text = (
            "# **تم تـ9فير بـ0ستات**\n\n"
            "**1 M0nth**\n"
            "**14 b00st**\n"
            "**~~22SAR~~**\n\n"
            "**3 M0nth**\n"
            "**14 b00st**\n"
            "**~~44SAR~~**\n\n"
            "**السعر الحالي**\n\n"
            "**1 M0nth**\n"
            "**14 b00st**\n"
            "**14SAR**\n\n"
            "**3 M0nth**\n"
            "**14 b00st**\n"
            "**22SAR**\n\n\n"
            "||@here @everyone||"
        )
        await interaction.response.send_message(details_text, ephemeral=True)


# أمر متجر البوستات (Slash Command)
@bot.tree.command(name="send_shop", description="يرسل متجر البوستات")
async def send_shop(interaction: discord.Interaction):
    embed = discord.Embed(
        title="اشتراكات",
        description="اضغط على زر ( عرض جميع التفاصيل )\n\nاضغط الزر بالأسفل لكامل التفاصيل",
        color=0xf1c40f
    )
    embed.set_image(url=SEPARATOR_IMAGE_URL)
    await interaction.response.send_message("✅ تم إرسال متجر البوستات بنجاح!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=BoostView())

# ==========================================
# 🎁 متجر النيترو
# ==========================================

class NitroView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        details_text = (
            "# **تم تـ9فير نيتر9 Gift**\n\n"
            "**Nitr0 M0nth**\n"
            "**12SAR**\n\n"
            "||@here @everyone||"
        )
        await interaction.response.send_message(details_text, ephemeral=True)


# أمر متجر النيترو (Slash Command)
@bot.tree.command(name="send_nitro", description="يرسل متجر النيترو")
async def send_nitro(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎁 نيترو",
        description="اضغط على زر ( عرض جميع التفاصيل )\n\nاضغط الزر بالأسفل لكامل التفاصيل",
        color=0xf1c40f
    )
    await interaction.response.send_message("✅ تم إرسال متجر النيترو بنجاح!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=NitroView())

# ==========================================
# 🖼️ الفاصل التلقائي بعد كل رسالة
# ==========================================

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if TARGET_CHANNEL_ID != 0 and message.channel.id == TARGET_CHANNEL_ID:
        embed = discord.Embed(color=message.author.color)
        embed.set_image(url=SEPARATOR_IMAGE_URL)
        await message.channel.send(embed=embed)

    await bot.process_commands(message)

# ==========================================
# ✅ تشغيل البوت ومزامنة الأوامر المائلة
# ==========================================

@bot.event
async def on_ready():
    bot.add_view(FeedbackView())
    bot.add_view(BoostView())
    bot.add_view(NitroView())
    bot.add_view(TicketDropdownView())
    bot.add_view(TicketControlView())
    
    # مزامنة السلاش كوماندز تلقائياً مع السيرفر
    try:
        synced = await bot.tree.sync()
        print(f"⚙️ تم مزامنة {len(synced)} من الأوامر المائلة (Slash Commands) بنجاح!")
    except Exception as e:
        print(f"❌ فشل مزامنة الأوامر: {e}")
        
    print(f'✅ تم تشغيل البوت بنجاح باسم: {bot.user}')
    await bot.change_presence(activity=discord.Game(name="DROYY "))

TOKEN = os.environ.get('DISCORD_TOKEN')
if __name__ == "__main__":
    bot.run(TOKEN)
