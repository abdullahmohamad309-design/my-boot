"""
Discord System Bot - Main File
بوت ديسكورد سيستم - الملف الرئيسي

Features: Moderation, Utility, Welcome, Logging, Tickets, Reaction Roles
"""

import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# تحميل المتغيرات من .env
load_dotenv()

# ============ الإعدادات ============
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", "!")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# ============ إعداد البوت ============
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.messages = True
intents.presences = False

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None,
    case_insensitive=True
)

# ============ عند تشغيل البوت ============
@bot.event
async def on_ready():
    print("=" * 50)
    print(f"✅ Bot Online: {bot.user.name}")
    print(f"🆔 Bot ID: {bot.user.id}")
    print(f"🌍 Servers: {len(bot.guilds)}")
    print(f"👥 Users: {sum(g.member_count for g in bot.guilds)}")
    print("=" * 50)

    # تغيير حالة البوت
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="!help | System Bot"
        ),
        status=discord.Status.online
    )

    # تحميل الـ Cogs
    await load_cogs()

async def load_cogs():
    """تحميل كل ملفات الـ Cogs"""
    cog_files = [
        "cogs.moderation",
        "cogs.utility",
        "cogs.welcome",
        "cogs.logging_system",
        "cogs.tickets",
        "cogs.setup",
        "cogs.reaction_roles"
    ]
    for cog in cog_files:
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded: {cog}")
        except Exception as e:
            print(f"❌ Failed to load {cog}: {e}")

# ============ أمر المساعدة ============
@bot.command(name="help", aliases=["مساعدة", "h"])
async def help_command(ctx):
    """عرض كل الأوامر | Show all commands"""
    embed = discord.Embed(
        title="🤖 System Bot | بوت سيستم",
        description="قائمة بجميع الأوامر المتاحة\nList of all available commands",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="🛡️ Moderation | الإدارة",
        value="`!kick`, `!ban`, `!unban`, `!mute`, `!unmute`, `!warn`, `!warnings`, `!clear`, `!lockdown`",
        inline=False
    )
    embed.add_field(
        name="📊 Utility | معلومات",
        value="`!ping`, `!serverinfo`, `!userinfo`, `!avatar`, `!roleinfo`, `!channelinfo`",
        inline=False
    )
    embed.add_field(
        name="👋 Welcome | الترحيب",
        value="`!setup welcome`, `!setup autorole`\nأوتوماتيك للأعضاء الجدد",
        inline=False
    )
    embed.add_field(
        name="📝 Logging | المراقبة",
        value="`!setup logs`, `!setup modlog`",
        inline=False
    )
    embed.add_field(
        name="🎫 Tickets | التذاكر",
        value="`!ticket` - فتح تكت | Open ticket\n`!close` - إغلاق | Close",
        inline=False
    )
    embed.add_field(
        name="📌 Reaction Roles | رتب بالتفاعل",
        value="`!rr add`, `!rr remove`, `!rr list`",
        inline=False
    )
    embed.add_field(
        name="🔧 Setup | الإعداد",
        value="`!setup` - عرض خيارات الإعداد",
        inline=False
    )

    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    await ctx.send(embed=embed)

# ============ أمر البينج ============
@bot.command(name="ping")
async def ping(ctx):
    """سرعة البوت | Bot latency"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"⚡ Latency: **{latency}ms**",
        color=discord.Color.green() if latency < 200 else discord.Color.orange()
    )
    await ctx.send(embed=embed)

# ============ تشغيل البوت ============
if __name__ == "__main__":
    if not TOKEN:
        print("❌ Error: DISCORD_TOKEN not found in .env file!")
        print("📝 Create a .env file and add your bot token.")
    else:
        bot.run(TOKEN)