import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# رابط الصورة الدائم
IMAGE_URL = "https://media.discordapp.net/attachments/1233857597143121920/1245084930121760818/image_2.png"

# ==========================================
# 1. نظام التقييم
# ==========================================
# ==========================================
# ⭐ نظام التقييم (مدمج وجاهز)
# ==========================================
class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="تقديم تقييم للمتجر")
        
        # خانة النجوم
        self.stars_input = TextInput(label="عدد النجوم (1-5)", placeholder="رقم من 1 إلى 5", min_length=1, max_length=1, required=True)
        self.add_item(self.stars_input)
        
        # خانة اسم المنتج
        self.product_input = TextInput(label="ما هو المنتج الذي اشتريته؟", placeholder="اكتب اسم المنتج هنا...", required=True)
        self.add_item(self.product_input)
        
        # خانة التعليق
        self.comment_input = TextInput(label="اكتب تقييمك هنا", style=discord.TextStyle.paragraph, required=True)
        self.add_item(self.comment_input)

    async def on_submit(self, interaction: discord.Interaction):
        stars_text = self.stars_input.value.strip()
        
        # التحقق من صحة النجوم
        if not stars_text.isdigit() or not (1 <= int(stars_text) <= 5):
            await interaction.response.send_message("❌ خطأ: يجب كتابة رقم من 1 إلى 5 في خانة النجوم!", ephemeral=True)
            return

        stars_number = int(stars_text)
        stars_emojis = "⭐" * stars_number

        # إنشاء الـ Embed (استخدام f""" لحل مشكلة كسر السطر)
        embed = discord.Embed(
            title="✨ شكراً على تقييمك !",
            description=f"""```\n• {self.comment_input.value}\n```""",
            color=0x808080
        )
        
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="⭐ تقييم الخدمة :", value=stars_emojis, inline=False)
        embed.add_field(name="📦 المنتج :", value=self.product_input.value, inline=False)
        embed.set_footer(text="Droy Store - نظام التقييمات")

        # إرسال للروم المخصص
        channel = interaction.client.get_channel(1508308686932803715)
        
        if channel:
            await channel.send(embed=embed)
            await interaction.response.send_message("✅ تم إرسال تقييمك بنجاح للروم المخصص!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ خطأ: لم يتم العثور على الروم المخصص لإرسال التقييم!", ephemeral=True)
class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="اضغط هنا للتقييم", style=discord.ButtonStyle.green, emoji="📝", custom_id="review_btn")
    async def open_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal())

# ==========================================
# 2. نظام المتجر
# ==========================================
class StoreView(View):
    def __init__(self, details, c_id):
        super().__init__(timeout=None)
        self.details = details
        self.show_details.custom_id = c_id

    @discord.ui.button(label="عرض جميع التفاصيل", style=discord.ButtonStyle.blurple, emoji="🛒")
    async def show_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.details, ephemeral=True)

# ==========================================
# 3. الأوامر (الاستجابة السريعة)
# ==========================================
@bot.tree.command(name="send_review", description="إرسال رسالة التقييم")
async def send_review(interaction: discord.Interaction):
    # نرد فوراً لتجنب خطأ عدم الاستجابة
    await interaction.response.send_message("جارٍ الإرسال...", ephemeral=True)
    embed = discord.Embed(title="⭐ نظام تقييمات Droy Store", description="عزيزي العميل، يسعدنا سماع رأيك في خدماتنا!", color=0x808080)
    embed.set_image(url=IMAGE_URL)
    await interaction.channel.send(embed=embed, view=FeedbackView())

@bot.tree.command(name="send_shop", description="إرسال متجر البوستات")
async def send_shop(interaction: discord.Interaction):
    await interaction.response.send_message("جارٍ الإرسال...", ephemeral=True)
    text = ("# **تم تـ9فير بـ0ستات**\n1 Month - 14SAR\n3 Month - 22SAR\n||@here @everyone||")
    embed = discord.Embed(title="🎁 البوستات", description="اضغط الزر بالأسفل للتفاصيل", color=0x808080)
    embed.set_image(url=IMAGE_URL)
    await interaction.channel.send(embed=embed, view=StoreView(text, "boost_btn"))

@bot.tree.command(name="send_nitro", description="إرسال متجر النيترو")
async def send_nitro(interaction: discord.Interaction):
    await interaction.response.send_message("جارٍ الإرسال...", ephemeral=True)
    text = ("# **تم تـ9فير نيتر9 Gift**\nNitro Month - 12SAR\n||@here @everyone||")
    embed = discord.Embed(title="🎁 نيترو", description="اضغط الزر بالأسفل للتفاصيل", color=0x808080)
    embed.set_image(url=IMAGE_URL)
    await interaction.channel.send(embed=embed, view=StoreView(text, "nitro_btn"))

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# كلاس زر الإغلاق
class CloseButton(View):
    def __init__(self, owner_id): # أضفنا owner_id هنا
        super().__init__(timeout=None)
        self.owner_id = owner_id # حفظ الـ ID

    @discord.ui.button(label="إغلاق التذكرة", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        admin_role_id = 1234567890 

        # التحقق من الرتبة أو أن المستخدم هو صاحب التذكرة
        if any(role.id == admin_role_id for role in interaction.user.roles) or interaction.user.id == self.owner_id:
            await interaction.response.send_message("سيتم إغلاق القناة في غضون 5 ثوانٍ...")
            await asyncio.sleep(5)
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("عذراً، ليس لديك صلاحية لإغلاق هذه التذكرة.", ephemeral=True)

# كلاس القائمة
class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="استفسار", value="inquiry"),
            discord.SelectOption(label="شراء منتج", value="purchase"),
        ]
        super().__init__(placeholder="أختر القائمة المناسبة لك", options=options)

    async def callback(self, interaction: discord.Interaction):
        # إنشاء القناة
        channel = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            overwrites={
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
        )

        embed = discord.Embed(
            title="نظام التذاكر",
            description=f"أهلاً {interaction.user.mention}، سيقوم فريق الدعم بمساعدتك قريباً.\n\nللإغلاق اضغط على الزر أدناه.",
            color=discord.Color.green()
        )

        # تمرير ID المستخدم للكلاس
        await channel.send(embed=embed, view=CloseButton(owner_id=interaction.user.id))
        await interaction.response.send_message(f"تم فتح تذكرتك: {channel.mention}", ephemeral=True)

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

--- الأوامر ---
@bot.tree.command(name="ticket", description="إرسال رسالة التذاكر")
async def ticket(interaction: discord.Interaction):
    embed = discord.Embed(title="تذكرة...", description="للطلب أو الاستفسار، افتح تذكرة عبر القائمة.", color=0x8B4513)
    await interaction.response.send_message(embed=embed, view=TicketView())

@bot.event
async def on_ready():
    # تسجيل الـ Views للعمل عند إعادة تشغيل البوت
    bot.add_view(CloseButton())
    bot.add_view(TicketView())
    await bot.tree.sync()
    print(f'البوت يعمل كـ {bot.user}')

bot.run(os.environ.get('DISCORD_TOKEN'))



@bot.event
async def on_ready():
    bot.add_view(FeedbackView())
    bot.add_view(StoreView("", "boost_btn"))
    bot.add_view(StoreView("", "nitro_btn"))
    print(f'✅ البوت يعمل: {bot.user}')

bot.run(os.environ.get('DISCORD_TOKEN'))
