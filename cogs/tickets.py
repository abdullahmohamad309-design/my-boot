"""
Ticket System Cog
نظام التذاكر
"""

import discord
from discord.ext import commands


class Tickets(commands.Cog):
    """🎫 نظام التذاكر | Ticket System"""

    def __init__(self, bot):
        self.bot = bot

    # ============ فتح تكت ============
    @commands.command(name="ticket", aliases=["تكت"])
    async def ticket(self, ctx):
        """فتح تكت دعم | Open a support ticket"""

        # تحقق إذا عنده تكت مفتوح
        existing = discord.utils.get(
            ctx.guild.text_channels,
            name=f"ticket-{ctx.author.name.lower().replace(' ', '-')}"
        )

        if existing:
            return await ctx.send(f"❌ عندك تكت مفتوح: {existing.mention} | You already have an open ticket.")

        # إنشاء القناة
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.author: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                attach_files=True,
                read_message_history=True
            ),
            ctx.guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_channels=True
            )
        }

        # إضافة صلاحية للإدارة
        for role in ctx.guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    manage_channels=True
                )

        try:
            channel = await ctx.guild.create_text_channel(
                name=f"ticket-{ctx.author.name}".lower().replace(" ", "-"),
                overwrites=overwrites,
                topic=f"Ticket by {ctx.author.id}"
            )

            embed = discord.Embed(
                title="🎫 Support Ticket | تكت دعم",
                description=f"مرحبا {ctx.author.mention}!\n\nشرح مشكلتك وراح يتم الرد عليك بأقرب وقت.\n\nWelcome {ctx.author.mention}!\nPlease describe your issue and staff will help you soon.",
                color=discord.Color.blue()
            )
            embed.add_field(name="📝 Close | إغلاق", value="استخدم `!close` لما تخلص | Use `!close` when done", inline=False)
            await channel.send(embed=embed)

            await ctx.send(f"✅ تم فتح تكت: {channel.mention} | Ticket opened.")
        except discord.Forbidden:
            await ctx.send("❌ ما عندي صلاحية أسوي قنوات | I lack permission to create channels.")

    # ============ إغلاق التكت ============
    @commands.command(name="close", aliases=["إغلاق"])
    async def close(self, ctx, reason="لم يذكر | Not specified"):
        if not ctx.channel.name.startswith("ticket-"):
            return await ctx.send("❌ هالأمر يشتغل بس بالتكتات | This command only works in tickets.")

        embed = discord.Embed(
            title="🔒 Closing Ticket | إغلاق التكت",
            description=f"سيتم إغلاق القناة خلال 5 ثواني...\nChannel will close in 5 seconds.\n\n**Reason | السبب:** {reason}",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

        await discord.utils.sleep_until(discord.utils.utcnow() + 5)

        try:
            await ctx.channel.delete(reason=f"Ticket closed by {ctx.author}")
        except discord.Forbidden:
            await ctx.send("❌ ما أقدر أحذف القناة | Cannot delete channel.")


async def setup(bot):
    await bot.add_cog(Tickets(bot))