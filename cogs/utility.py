"""
Utility Cog
أوامر المعلومات والمساعدة
"""

import discord
from discord.ext import commands
from datetime import datetime


class Utility(commands.Cog):
    """📊 أوامر المعلومات | Utility Commands"""

    def __init__(self, bot):
        self.bot = bot

    # ============ Ping ============
    @commands.command(name="ping2", aliases=["بينج"])
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"⚡ Latency | السرعة: **{latency}ms**",
            color=discord.Color.green() if latency < 200 else discord.Color.orange()
        )
        await ctx.send(embed=embed)

    # ============ Server Info ============
    @commands.command(name="serverinfo", aliases=["معلومات_السيرفر", "server"])
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
            title=f"📊 {guild.name}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(name="👑 Owner | المالك", value=guild.owner.mention if guild.owner else "N/A", inline=True)
        embed.add_field(name="👥 Members | الأعضاء", value=guild.member_count, inline=True)
        embed.add_field(name="💬 Channels | القنوات", value=len(guild.channels), inline=True)
        embed.add_field(name="🎭 Roles | الرتب", value=len(guild.roles), inline=True)
        embed.add_field(name="😀 Emojis | الإيموجي", value=len(guild.emojis), inline=True)
        embed.add_field(name="📅 Created | انشئ", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="🆔 ID", value=guild.id, inline=False)
        await ctx.send(embed=embed)

    # ============ User Info ============
    @commands.command(name="userinfo", aliases=["معلومات", "user", "whois"])
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title=f"👤 {member}",
            color=member.color,
            timestamp=datetime.utcnow()
        )
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        embed.add_field(name="🆔 ID", value=member.id, inline=True)
        embed.add_field(name="📛 Nickname | الاسم المستعار", value=member.nick or "None", inline=True)
        embed.add_field(name="🤖 Bot?", value="Yes" if member.bot else "No", inline=True)
        embed.add_field(name="📅 Joined | انضم", value=member.joined_at.strftime("%Y-%m-%d") if member.joined_at else "N/A", inline=True)
        embed.add_field(name="📅 Account Created | إنشاء الحساب", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name=f"🎭 Roles | الرتب ({len(member.roles) - 1})", value=", ".join([r.mention for r in member.roles[1:5]]) or "None", inline=False)
        await ctx.send(embed=embed)

    # ============ Avatar ============
    @commands.command(name="avatar", aliases=["صورة", "av"])
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        if not member.avatar:
            return await ctx.send("❌ ما عنده صورة | No avatar.")

        embed = discord.Embed(
            title=f"🖼️ {member}'s Avatar | صورة {member}",
            color=discord.Color.purple()
        )
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    # ============ Role Info ============
    @commands.command(name="roleinfo", aliases=["رتبة"])
    async def roleinfo(self, ctx, role: discord.Role = None):
        if not role:
            return await ctx.send("❌ `!roleinfo @role`")

        embed = discord.Embed(
            title=f"🎭 Role: {role.name}",
            color=role.color
        )
        embed.add_field(name="🆔 ID", value=role.id, inline=True)
        embed.add_field(name="👥 Members | الأعضاء", value=len(role.members), inline=True)
        embed.add_field(name="📅 Created | الانشاء", value=role.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="🔢 Position | الموقع", value=role.position, inline=True)
        embed.add_field(name="💬 Mentionable | قابل للذكر", value="Yes" if role.mentionable else "No", inline=True)
        embed.add_field(name="🔒 Hoisted | منفصلة", value="Yes" if role.hoist else "No", inline=True)
        await ctx.send(embed=embed)

    # ============ Channel Info ============
    @commands.command(name="channelinfo", aliases=["قناة"])
    async def channelinfo(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        embed = discord.Embed(
            title=f"💬 #{channel.name}",
            color=discord.Color.teal()
        )
        embed.add_field(name="🆔 ID", value=channel.id, inline=True)
        embed.add_field(name="📁 Category | القسم", value=channel.category.name if channel.category else "None", inline=True)
        embed.add_field(name="📅 Created | الانشاء", value=channel.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="🔞 NSFW?", value="Yes" if channel.nsfw else "No", inline=True)
        embed.add_field(name="📝 Topic | الموضوع", value=channel.topic or "None", inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Utility(bot))