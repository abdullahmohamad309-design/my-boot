"""
Welcome System Cog
نظام الترحيب والأوتو رول
"""

import json
import os
import discord
from discord.ext import commands

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
WELCOME_FILE = os.path.join(DATA_DIR, "welcome.json")


class Welcome(commands.Cog):
    """👋 نظام الترحيب | Welcome System"""

    def __init__(self, bot):
        self.bot = bot

    def load_config(self):
        """تحميل الإعدادات"""
        if not os.path.exists(WELCOME_FILE):
            return {}
        try:
            with open(WELCOME_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def save_config(self, data):
        """حفظ الإعدادات"""
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(WELCOME_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ============ عند دخول عضو جديد ============
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return

        config = self.load_config()
        guild_config = config.get(str(member.guild.id), {})

        # Auto-role
        autorole_id = guild_config.get("autorole")
        if autorole_id:
            role = member.guild.get_role(autorole_id)
            if role:
                try:
                    await member.add_roles(role, reason="Auto-role on join")
                except discord.Forbidden:
                    pass

        # Welcome message
        welcome_channel_id = guild_config.get("welcome_channel")
        if welcome_channel_id:
            channel = member.guild.get_channel(welcome_channel_id)
            if channel:
                embed = discord.Embed(
                    title="👋 Welcome! | أهلاً وسهلاً!",
                    description=f"مرحبا {member.mention} في **{member.guild.name}**!\n\nWelcome {member.mention} to **{member.guild.name}**!",
                    color=discord.Color.green(),
                    timestamp=discord.utils.utcnow()
                )
                if member.avatar:
                    embed.set_thumbnail(url=member.avatar.url)
                embed.add_field(name="👥 Member # | العضو رقم", value=member.guild.member_count, inline=True)
                embed.set_footer(text=member.guild.name, icon_url=member.guild.icon.url if member.guild.icon else None)
                try:
                    await channel.send(embed=embed)
                except discord.Forbidden:
                    pass

    # ============ عند خروج عضو ============
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            return

        config = self.load_config()
        guild_config = config.get(str(member.guild.id), {})
        leave_channel_id = guild_config.get("leave_channel")

        if leave_channel_id:
            channel = member.guild.get_channel(leave_channel_id)
            if channel:
                embed = discord.Embed(
                    title="😢 Goodbye | مع السلامة",
                    description=f"**{member.name}** غادر السيرفر.\n**{member.name}** has left the server.",
                    color=discord.Color.red(),
                    timestamp=discord.utils.utcnow()
                )
                if member.avatar:
                    embed.set_thumbnail(url=member.avatar.url)
                try:
                    await channel.send(embed=embed)
                except discord.Forbidden:
                    pass


async def setup(bot):
    await bot.add_cog(Welcome(bot))