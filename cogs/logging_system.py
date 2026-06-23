"""
Logging System Cog
نظام المراقبة واللوجز
"""

import json
import os
import discord
from discord.ext import commands

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
LOG_FILE = os.path.join(DATA_DIR, "logs.json")


class LoggingSystem(commands.Cog):
    """📝 نظام اللوجز | Logging System"""

    def __init__(self, bot):
        self.bot = bot

    def load_config(self):
        if not os.path.exists(LOG_FILE):
            return {}
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    async def get_log_channel(self, guild_id):
        config = self.load_config()
        channel_id = config.get(str(guild_id), {}).get("log_channel")
        if channel_id:
            channel = self.bot.get_channel(channel_id)
            return channel
        return None

    # ============ تعديل رسالة ============
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return

        channel = await self.get_log_channel(before.guild.id)
        if not channel:
            return

        embed = discord.Embed(
            title="✏️ Message Edited | رسالة معدلة",
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="👤 Author | الكاتب", value=before.author.mention, inline=True)
        embed.add_field(name="💬 Channel | القناة", value=before.channel.mention, inline=True)
        embed.add_field(name="📝 Before | قبل", value=before.content[:1024] or "Empty", inline=False)
        embed.add_field(name="📝 After | بعد", value=after.content[:1024] or "Empty", inline=False)
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass

    # ============ حذف رسالة ============
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        channel = await self.get_log_channel(message.guild.id)
        if not channel:
            return

        embed = discord.Embed(
            title="🗑️ Message Deleted | رسالة محذوفة",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="👤 Author | الكاتب", value=message.author.mention, inline=True)
        embed.add_field(name="💬 Channel | القناة", value=message.channel.mention, inline=True)
        embed.add_field(name="📝 Content | المحتوى", value=message.content[:1024] or "Empty", inline=False)
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass

    # ============ دخول عضو ============
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return

        channel = await self.get_log_channel(member.guild.id)
        if not channel:
            return

        embed = discord.Embed(
            title="📥 Member Joined | عضو دخل",
            description=f"{member.mention} | {member}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="🆔 ID", value=member.id, inline=True)
        embed.add_field(name="👥 Count | العدد", value=member.guild.member_count, inline=True)
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass

    # ============ خروج عضو ============
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            return

        channel = await self.get_log_channel(member.guild.id)
        if not channel:
            return

        embed = discord.Embed(
            title="📤 Member Left | عضو خرج",
            description=f"{member} | {member.id}",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="👥 Count | العدد", value=member.guild.member_count, inline=True)
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass

    # ============ تغيير اسم العضو ============
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            channel = await self.get_log_channel(before.guild.id)
            if not channel:
                return

            embed = discord.Embed(
                title="📝 Nickname Changed | تغيير اسم مستعار",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="👤 Member", value=after.mention, inline=False)
            embed.add_field(name="📝 Before | قبل", value=before.nick or "None", inline=True)
            embed.add_field(name="📝 After | بعد", value=after.nick or "None", inline=True)
            try:
                await channel.send(embed=embed)
            except discord.Forbidden:
                pass


async def setup(bot):
    await bot.add_cog(LoggingSystem(bot))