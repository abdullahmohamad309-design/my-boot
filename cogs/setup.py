"""
Setup Cog
أوامر إعداد السيرفر
"""

import json
import os
import discord
from discord.ext import commands

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
WELCOME_FILE = os.path.join(DATA_DIR, "welcome.json")
LOG_FILE = os.path.join(DATA_DIR, "logs.json")


class Setup(commands.Cog):
    """🔧 أوامر الإعداد | Setup Commands"""

    def __init__(self, bot):
        self.bot = bot

    def load_json(self, filepath):
        if not os.path.exists(filepath):
            return {}
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def save_json(self, filepath, data):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ============ Setup Menu ============
    @commands.group(name="setup", aliases=["إعداد"], invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        embed = discord.Embed(
            title="🔧 Setup Menu | قائمة الإعداد",
            description="الأوامر الفرعية | Subcommands:",
            color=discord.Color.gold()
        )
        embed.add_field(name="📥 Welcome", value="`!setup welcome #channel` - قناة الترحيب", inline=False)
        embed.add_field(name="📤 Leave", value="`!setup leave #channel` - قناة المغادرة", inline=False)
        embed.add_field(name="🎭 AutoRole", value="`!setup autorole @role` - رتبة تلقائية", inline=False)
        embed.add_field(name="📝 Logs", value="`!setup logs #channel` - قناة اللوجز", inline=False)
        embed.add_field(name="🛡️ ModLog", value="`!setup modlog #channel` - قناة المودريشن", inline=False)
        await ctx.send(embed=embed)

    # ============ Welcome Channel ============
    @setup.command(name="welcome")
    @commands.has_permissions(administrator=True)
    async def setup_welcome(self, ctx, channel: discord.TextChannel):
        data = self.load_json(WELCOME_FILE)
        data.setdefault(str(ctx.guild.id), {})["welcome_channel"] = channel.id
        self.save_json(WELCOME_FILE, data)
        embed = discord.Embed(
            title="✅ Welcome Channel Set",
            description=f"قناة الترحيب: {channel.mention}\nWelcome channel: {channel.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    # ============ Leave Channel ============
    @setup.command(name="leave")
    @commands.has_permissions(administrator=True)
    async def setup_leave(self, ctx, channel: discord.TextChannel):
        data = self.load_json(WELCOME_FILE)
        data.setdefault(str(ctx.guild.id), {})["leave_channel"] = channel.id
        self.save_json(WELCOME_FILE, data)
        embed = discord.Embed(
            title="✅ Leave Channel Set",
            description=f"قناة المغادرة: {channel.mention}\nLeave channel: {channel.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    # ============ Auto Role ============
    @setup.command(name="autorole")
    @commands.has_permissions(administrator=True)
    async def setup_autorole(self, ctx, role: discord.Role):
        data = self.load_json(WELCOME_FILE)
        data.setdefault(str(ctx.guild.id), {})["autorole"] = role.id
        self.save_json(WELCOME_FILE, data)
        embed = discord.Embed(
            title="✅ Auto Role Set",
            description=f"الرتبة التلقائية: {role.mention}\nAuto role: {role.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    # ============ Logs Channel ============
    @setup.command(name="logs")
    @commands.has_permissions(administrator=True)
    async def setup_logs(self, ctx, channel: discord.TextChannel):
        data = self.load_json(LOG_FILE)
        data.setdefault(str(ctx.guild.id), {})["log_channel"] = channel.id
        self.save_json(LOG_FILE, data)
        embed = discord.Embed(
            title="✅ Logs Channel Set",
            description=f"قناة اللوجز: {channel.mention}\nLogs channel: {channel.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Setup(bot))