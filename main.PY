import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput, Select
import asyncio
import os
import random  # أضفنا مكتبة الراندوم لحساب أرقام التيكت من 1 إلى 9999

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # مهمة للتحكم برومات التيكت وصلاحياتها
allowed_mentions = discord.AllowedMentions(everyone=True, roles=True, users=True)
bot = commands.Bot(command_prefix="!", intents=intents, allowed_mentions=allowed_mentions)

# ==========================================
# ⚙️ الإعدادات — عدّلها حسب حاجتك
# ==========================================

# آيدي روم الفاصل التلقائي (ضع 0 لتعطيله)
TARGET_CHANNEL_ID = 1508308686932803715 

# رابط صورة الفاصل الأسود (Droy Store)
SEPARATOR_IMAGE_URL = "https://media.discordapp.net/attachments/1233857597143121920/1245091722830811218/cdf7074f1d9df649.png"

# 🎫 إعدادات نظام التيكت (ضع الآيديهات الخاصة بسيرفرك هنا)
OPEN_TICKETS_CATEGORY_ID = 123456789012345678    # آيدي كاتيغوري التيكتات المفتوحة
CLOSED_TICKETS_CATEGORY_ID = 876543210987654321  # آيدي كاتيغوري التيكتات المقفلة
STAFF_ROLE_ID = 112233445566778899               # آيدي رتبة الدعم الفني (الستاف)

# ==========================================
# 🎫 نظام التيكت (Ticket System) — الجديد
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
        
        # تعديل اسم الروم ليصبح قبله علامة القفل
        new_name = f"🔒-{channel.name}"
        
        # سحب صلاحية الكتابة من الأعضاء وابقائها للستاف
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        await channel.edit(name=new_name, category=closed_category, overwrites=overwrites)
        
        # رسالة الإغلاق باللون الرصاصي التصميمي
        embed_closed = discord.Embed(
            description="🔒 **تم إغلاق التذكرة بنجاح وتحويلها للأرشيف.**",
            color=0x7f8c8d
        )
        await channel.send(embed=embed_closed)


class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="شراء منتجات المتجر", 
                description="لشراء منتجات المتجر اضغط على هذا الخيار", 
                emoji="🛒", 
                value="buy"
            ),
            discord.SelectOption(
                label="استفسار", 
                description="للاستفسار اضغط على هذا الخيار", 
                emoji="❓", 
                value="info"
            )
        ]
        super().__init__(placeholder="اضغط هنا لاختيار نوع التذكرة...", min_values=1, max_values=1, custom_id="ticket_select_menu")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        staff_role = guild.get_role(STAFF_ROLE_ID)
        open_category = guild.get_channel(OPEN_TICKETS_CATEGORY_ID)
        
        # عدّاد عشوائي للتيكت من 1 إلى 9999
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

        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            category=open_category,
            overwrites=overwrites
        )

        await interaction.response.send_message(f"✅ تم فتح تذكرتك بنجاح: {ticket_channel.mention}", ephemeral=True)

        # رسالة ترحيبية باللون الرصاصي التصميمي
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


@bot.command()
@commands.has_permissions(administrator=True)
async def send_ticket(ctx):
    """يرسل بنل التيكت القائمة المنسدلة (للإدارة فقط)"""
    embed_panel = discord.Embed(
        title="🎫 مركز الدعم الفني | Droy Store",
        description="أهلاً بك في مركز المساعدة الخاص بمتجرنا.\n\nالرجاء اختيار القسم المناسب من القائمة بالأسفل لفتح تذكرة جديدة.",
        color=0x7f8c8d
    )
    await ctx.send(embed=embed_panel, view=TicketDropdownView())
    await ctx.message.delete()

# ==========================================
# ⭐ نظام التقييم — Droy Store
# ==========================================

class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="تقديم تقييم للمتجر")

        self.stars_input = TextInput(
            label="عدد النجوم (من 1 إلى 5)",
            placeholder="اكتب رقم من 1 إلى 5 فقط...",
            min_length=1,
            max_length=1,
            required=True
        )
        self.add_item(self.stars_input)

        self.comment_input = TextInput(
            label="اكتب تقييمك هنا",
            style=discord.TextStyle.paragraph,
            placeholder="اكتب رأيك بالخدمة أو المنتج...",
            min_length=3,
            max_length=500,
            required=True
        )
        self.add_item(self.comment_input)

    async def on_submit(self, interaction: discord.Interaction):
        stars_text = self.stars_input.value.strip()
        comment = self.comment_input.value

        if not stars_text.isdigit() or not (1 <= int(stars_text) <= 5):
            await interaction.response.send_message(
                "❌ خطأ: يجب أن تكتب رقماً من 1 إلى 5 فقط في خانة النجوم!",
                ephemeral=True
            )
            return

        stars_number = int(stars_text)
        stars_emojis = "⭐" * stars_number

        embed = discord.Embed(
            title="✨ شكراً على تقييمك!",
            description=f"\n```\n• {comment}\n
```",
            color=0x5c3a75
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url
        )
        embed.add_field(name="⭐ تقييم الخدمة :", value=stars_emojis, inline=True)
        embed.add_field(name="📦 المنتج :", value="خدمة / منتج من المتجر", inline=True)
        embed.set_footer(text="Droy Store - نظام التقييمات")

        await interaction.channel.send(embed=embed)
        await interaction.response.send_message(
            "✅ تم إرسال تقييمك بنجاح، شكراً لك!",
            ephemeral=True
        )


class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="اضغط هنا للتقييم", style=discord.ButtonStyle.green, emoji="📝")
    async def open_feedback_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal())


@bot.command()
async def send_review(ctx):
    """يرسل رسالة التقييم الثابتة مع الزر"""
    embed = discord.Embed(
        title="⭐ نظام تقييمات Droy Store",
        description="عزيزي العميل، يسعدنا سماع رأيك في خدماتنا!\n\nاضغط على الزر بالأسفل لتقديم تقييمك بخصوص الخدمة.",
        color=0x5c3a75
    )
    await ctx.send(embed=embed, view=FeedbackView())


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


@bot.command()
async def send_shop(ctx):
    """يرسل متجر البوستات"""
    embed = discord.Embed(
        title="اشتراكات",
        description="اضغط على زر ( عرض جميع التفاصيل )\n\nاضغط الزر بالأسفل لكامل التفاصيل",
        color=0xf1c40f
    )
    embed.set_image(url=SEPARATOR_IMAGE_URL)
    await ctx.send(embed=embed, view=BoostView())


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


@bot.command()
async def send_nitro(ctx):
    """يرسل متجر النيترو"""
    embed = discord.Embed(
        title="🎁 نيترو",
        description="اضغط على زر ( عرض جميع التفاصيل )\n\nاضغط الزر بالأسفل لكامل التفاصيل",
        color=0xf1c40f
    )
    await ctx.send(embed=embed, view=NitroView())


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
# ✅ تشغيل البوت
# ==========================================

@bot.event
async def on_ready():
    # تسجيل الـ Views عشان تظل الأزرار والقوائم شغالة حتى لو رستر البوت
    bot.add_view(FeedbackView())
    bot.add_view(BoostView())
    bot.add_view(NitroView())
    bot.add_view(TicketDropdownView())
    bot.add_view(TicketControlView())
    
    print(f'✅ تم تشغيل البوت بنجاح باسم: {bot.user}')
    await bot.change_presence(activity=discord.Game(name=" droyy 🚀"))

# السطر الخاص بالتوكن كما هو بدون تعديل
TOKEN = os.environ.get('DISCORD_TOKEN')
if __name__ == "__main__":
    bot.run(TOKEN)
