"""
Reaction Roles Cog
نظام الرتب بالتفاعل
"""

import json
import os
import discord
from discord.ext import commands

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
RR_FILE = os.path.join(DATA_DIR, "reaction_roles.json")


class ReactionRoles(commands.Cog):
    """📌 نظام الرتب بالتفاعل | Reaction Roles"""

    def __init__(self, bot):
        self.bot = bot

    def load_config(self):
        if not os.path.exists(RR_FILE):
            return {}
        try:
            with open(RR_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def save_config(self, data):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(RR_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ============ Group Command ============
    @commands.group(name="rr", aliases=["رتب"], invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def rr(self, ctx):
        embed = discord.Embed(
            title="📌 Reaction Roles | رتب التفاعل",
            description="`!rr add [message_id] [emoji] @role`\n`!rr remove [message_id]`\n`!rr list`",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

    # ============ Add ============
    @rr.command(name="add")
    @commands.has_permissions(administrator=True)
    async def rr_add(self, ctx, message_id: int, emoji: str, role: discord.Role):
        try:
            message = await ctx.channel.fetch_message(message_id)
        except discord.NotFound:
            return await ctx.send("❌ ما لقيت الرسالة | Message not found.")

        await message.add_reaction(emoji)

        data = self.load_config()
        guild_id = str(ctx.guild.id)
        msg_id = str(message_id)

        if guild_id not in data:
            data[guild_id] = {}
        if msg_id not in data[guild_id]:
            data[guild_id][msg_id] = []

        data[guild_id][msg_id].append({"emoji": emoji, "role_id": role.id})
        self.save_config(data)

        embed = discord.Embed(
            title="✅ Reaction Role Added",
            description=f"اضغط {emoji} لتحصل على {role.mention}\nReact with {emoji} to get {role.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    # ============ Remove ============
    @rr.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def rr_remove(self, ctx, message_id: int):
        data = self.load_config()
        guild_id = str(ctx.guild.id)
        msg_id = str(message_id)

        if guild_id in data and msg_id in data[guild_id]:
            del data[guild_id][msg_id]
            self.save_config(data)
            await ctx.send("✅ تم حذف الرتب التفاعلية | Reaction roles removed.")
        else:
            await ctx.send("❌ ما لقيت رتب تفاعلية بهالرسالة | Not found.")

    # ============ List ============
    @rr.command(name="list")
    async def rr_list(self, ctx):
        data = self.load_config()
        guild_id = str(ctx.guild.id)

        if guild_id not in data or not data[guild_id]:
            return await ctx.send("❌ ما في رتب تفاعلية | No reaction roles set.")

        embed = discord.Embed(title="📌 Reaction Roles List", color=discord.Color.purple())
        for msg_id, reactions in data[guild_id].items():
            value = ""
            for r in reactions:
                role = ctx.guild.get_role(r["role_id"])
                role_name = role.mention if role else "Unknown"
                value += f"{r['emoji']} → {role_name}\n"
            embed.add_field(name=f"Message: {msg_id}", value=value or "Empty", inline=False)

        await ctx.send(embed=embed)

    # ============ Listener: عند التفاعل ============
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member and payload.member.bot:
            return

        data = self.load_config()
        guild_id = str(payload.guild_id)
        msg_id = str(payload.message_id)
        emoji = str(payload.emoji)

        if guild_id not in data or msg_id not in data[guild_id]:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        for rr in data[guild_id][msg_id]:
            if rr["emoji"] == emoji:
                role = guild.get_role(rr["role_id"])
                if role:
                    try:
                        await payload.member.add_roles(role, reason="Reaction role")
                    except discord.Forbidden:
                        pass

    # ============ Listener: عند إزالة التفاعل ============
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        data = self.load_config()
        guild_id = str(payload.guild_id)
        msg_id = str(payload.message_id)
        emoji = str(payload.emoji)

        if guild_id not in data or msg_id not in data[guild_id]:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        member = guild.get_member(payload.user_id)
        if not member:
            return

        for rr in data[guild_id][msg_id]:
            if rr["emoji"] == emoji:
                role = guild.get_role(rr["role_id"])
                if role:
                    try:
                        await member.remove_roles(role, reason="Reaction role removed")
                    except discord.Forbidden:
                        pass


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))