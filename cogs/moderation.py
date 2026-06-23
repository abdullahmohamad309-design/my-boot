"""
Moderation Cog
أوامر الإدارة
"""

import json
import os
import discord
from discord.ext import commands
from datetime import timedelta, datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
WARNS_FILE = os.path.join(DATA_DIR, "warnings.json")


class Moderation(commands.Cog):
    """🛡️ أوامر الإدارة | Moderation Commands"""

    def __init__(self, bot):
        self.bot = bot

    # ============ Kick ============
    @commands.command(name="kick", aliases=["طرد"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason="لم يذكر | Not specified"):
        if not member:
            embed = discord.Embed(
                title="❌ Usage | الاستخدام",
                description="`!kick @user [reason]`",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)

        if member.top_role >= ctx.author.top_role:
            return await ctx.send("❌ ما تقدر تطرد شخص رتبته أعلى منك | Cannot kick higher role.")

        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="👢 Kick | طرد",
                description=f"**User | العضو:** {member.mention}\n**Reason | السبب:** {reason}\n**By | بواسطة:** {ctx.author.mention}",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ ما عندي صلاحية أطرده | I lack permission.")

    # ============ Ban ============
    @commands.command(name="ban", aliases=["حظر"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason="لم يذكر | Not specified"):
        if not member:
            embed = discord.Embed(
                title="❌ Usage | الاستخدام",
                description="`!ban @user [reason]`",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)

        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="🔨 Ban | حظر",
                description=f"**User | العضو:** {member.mention}\n**Reason | السبب:** {reason}\n**By | بواسطة:** {ctx.author.mention}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ ما عندي صلاحية أحظره | I lack permission.")

    # ============ Unban ============
    @commands.command(name="unban", aliases=["رفع_حظر"])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int = None):
        if not user_id:
            return await ctx.send("❌ `!unban [user_id]`")

        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            embed = discord.Embed(
                title="✅ Unban | رفع حظر",
                description=f"**User | العضو:** {user.mention}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except discord.NotFound:
            await ctx.send("❌ ما لقيت الحظر | Ban not found.")
        except discord.Forbidden:
            await ctx.send("❌ ما عندي صلاحية | I lack permission.")

    # ============ Mute (Timeout) ============
    @commands.command(name="mute", aliases=["كتم"])
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member = None, duration: str = "10m", *, reason="لم يذكر | Not specified"):
        if not member:
            return await ctx.send("❌ `!mute @user [duration] [reason]`\n**مثال:** `!mute @user 1h`")

        # تحويل الوقت
        time_units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        try:
            unit = duration[-1].lower()
            value = int(duration[:-1])
            seconds = value * time_units.get(unit, 60)
        except:
            seconds = 600  # default 10 min

        try:
            until = discord.utils.utcnow() + timedelta(seconds=seconds)
            await member.timeout(until, reason=reason)
            embed = discord.Embed(
                title="🔇 Mute | كتم",
                description=f"**User | العضو:** {member.mention}\n**Duration | المدة:** {duration}\n**Reason | السبب:** {reason}",
                color=discord.Color.greyple()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ ما عندي صلاحية أكتمه | I lack permission.")

    # ============ Unmute ============
    @commands.command(name="unmute", aliases=["فك_كتم"])
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member = None):
        if not member:
            return await ctx.send("❌ `!unmute @user`")

        try:
            await member.timeout(None)
            embed = discord.Embed(
                title="🔊 Unmute | فك كتم",
                description=f"**User | العضو:** {member.mention}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ ما عندي صلاحية | I lack permission.")

    # ============ Warn ============
    @commands.command(name="warn", aliases=["تحذير"])
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member = None, *, reason="لم يذكر | Not specified"):
        if not member:
            return await ctx.send("❌ `!warn @user [reason]`")

        # تحميل التحذيرات
        data = {}
        if os.path.exists(WARNS_FILE):
            try:
                with open(WARNS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except:
                data = {}

        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        if guild_id not in data:
            data[guild_id] = {}
        if user_id not in data[guild_id]:
            data[guild_id][user_id] = []

        warn_entry = {
            "reason": reason,
            "mod": str(ctx.author.id),
            "time": datetime.utcnow().isoformat()
        }
        data[guild_id][user_id].append(warn_entry)

        os.makedirs(DATA_DIR, exist_ok=True)
        with open(WARNS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        warn_count = len(data[guild_id][user_id])
        embed = discord.Embed(
            title="⚠️ Warning | تحذير",
            description=f"**User | العضو:** {member.mention}\n**Reason | السبب:** {reason}\n**Total Warnings | عدد التحذيرات:** {warn_count}",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    # ============ Warnings List ============
    @commands.command(name="warnings", aliases=["تحذيرات"])
    @commands.has_permissions(kick_members=True)
    async def warnings(self, ctx, member: discord.Member = None):
        if not member:
            return await ctx.send("❌ `!warnings @user`")

        data = {}
        if os.path.exists(WARNS_FILE):
            try:
                with open(WARNS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except:
                data = {}

        warns = data.get(str(ctx.guild.id), {}).get(str(member.id), [])

        if not warns:
            return await ctx.send(f"✅ {member.mention} ما عنده تحذيرات | No warnings.")

        embed = discord.Embed(
            title=f"⚠️ Warnings for {member}",
            color=discord.Color.gold()
        )
        for i, w in enumerate(warns, 1):
            mod = ctx.guild.get_member(int(w["mod"]))
            mod_name = mod.mention if mod else "Unknown"
            embed.add_field(
                name=f"#{i} | {w['time'][:10]}",
                value=f"**Reason:** {w['reason']}\n**By:** {mod_name}",
                inline=False
            )
        embed.set_footer(text=f"Total: {len(warns)} | المجموع")
        await ctx.send(embed=embed)

    # ============ Clear Messages ============
    @commands.command(name="clear", aliases=["مسح"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = None):
        if not amount:
            return await ctx.send("❌ `!clear [number]`")
        if amount > 100:
            amount = 100

        try:
            deleted = await ctx.channel.purge(limit=amount + 1)
            msg = await ctx.send(f"✅ تم مسح {len(deleted) - 1} رسالة | Cleared {len(deleted) - 1} messages")
            await msg.delete(delay=3)
        except discord.Forbidden:
            await ctx.send("❌ ما عندي صلاحية أمسح الرسائل | I lack permission.")

    # ============ Lockdown ============
    @commands.command(name="lockdown", aliases=["قفل"])
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        try:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            embed = discord.Embed(
                title="🔒 Locked | مقفل",
                description=f"{channel.mention} تم قفلها | Channel locked.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ ما عندي صلاحية أقفل القناة | I lack permission.")

    @commands.command(name="unlock", aliases=["فتح"])
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        try:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            embed = discord.Embed(
                title="🔓 Unlocked | مفتوح",
                description=f"{channel.mention} تم فتحها | Channel unlocked.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ ما عندي صلاحية أفتح القناة | I lack permission.")


async def setup(bot):
    await bot.add_cog(Moderation(bot))