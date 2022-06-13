from ast import alias
import imp
import disnake
from disnake.ext import commands
import json
from datetime import datetime
import time
from constants import C_INVISIBLE, C_MAIN


class Utility(commands.Cog):
    def __init__(self , bot):
        self.bot = bot
        self.hidden = False
        self.emoji = "꒰ <:AEmiThinkC:943366254243233822> ꒱"
        self.description = "Includes Utility Related Commands."

    @commands.command(name="ping", description="Shows Ping/Response Time of the bot.", aliases=["status"])
    async def ping(self, ctx):
        before = time.monotonic()
        msg = await ctx.channel.send("\`🏓\` **- Getting my ping ...**")
        ping = (time.monotonic() - before) * 1000
        await msg.delete()
        emb = disnake.Embed(color=C_MAIN, description=f":heartpulse: Command: `{round(ping)} ms` \n:stopwatch: Gateway: `{round(self.bot.latency * 1000)} ms`")
        emb.set_author(name=f"{self.bot.user.name}", icon_url=self.bot.user.avatar.url)
        await ctx.channel.send(embed=emb)

    @commands.command(name="userinfo", usage=f"`< user >`", description=f"Shows UserInfo with Roles.", aliases = ["whois"])
    @commands.guild_only()
    async def userinfo(self, ctx, member: disnake.Member=None):
        if member is None:
            member = ctx.author
        created_at = member.created_at.strftime("%b %d, %Y")
        joined_at = member.joined_at.strftime("%b %d, %Y")
        rolesMention = [role.mention for role in member.roles]
        rolesMention.pop(0)
        rolesMention.reverse()
        noPermList =  ['Create Instant Invite',  'Add Reactions',  'Priority Speaker', 'Stream', 'Read Messages', 'Send Messages', 'Send TTS Messages', 'Embed Links', 'Attach Files', 'Read Message History', 'Connect', 'Speak',  'Use Voice Activation',  'Use Slash Commands', 'Request To Speak']
        permList = [p[0].replace('_',' ').replace('guild', 'server').title().replace('Tts','TTS') for p in member.guild_permissions if p[1]]
        
        for perm in noPermList:
            if perm in permList:
                permList.remove(perm)
        admin = False
        mod = False
        manager = False
        memberA=False
        if  "Administrator" in permList:
            admin = True
        elif "Manage Server" in permList:
            manager = True
        elif "Mute Members" in permList:
            mod = True
        else:
            memberA = True
        text=', '.join(permList)
        
        embed = disnake.Embed(description=f"{member.mention} `[{member.id}]`", color=ctx.author.color)
        embed.add_field(name="`📆` `Created`", value=f"**- `{created_at}`**\n`")
        embed.add_field(name="`📅` `Joined`", value=f"**- `{joined_at}`**\n")
        if member.avatar.is_animated():
            embed.add_field(name="`📱` `Avatar`", value=f"[Animated]({member.avatar.url})", inline=False)
        if not member.avatar.is_animated():
            embed.add_field(name="`📱` `Avatar`", value=f"[Non-Animated]({member.avatar.url})", inline=False)
        embed.add_field(name=f"`ℹ` `Roles [{len(rolesMention)}]`", value=" ".join(rolesMention), inline=False)
        if not memberA:
            embed.add_field(name="`📱` `Key Permissions`", value=text, inline=False)
        if admin:
            embed.add_field(name="`📱` `Acknowledgements`", value="**- `Server Admin`**\n\n", inline=False)
        if manager:
            embed.add_field(name="`📱` `Acknowledgements`", value="**- `Server Manager`**\n\n", inline=False)
        if mod:
            embed.add_field(name="`📱` `Acknowledgements`", value="**- `Server Moderator`**\n\n", inline=False)
        embed.set_author(icon_url=ctx.author.avatar.url, name=ctx.author)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text="Team Tatsui ❤️")
        embed.timestamp =  datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(description=f"Shows Server Info", name="serverinfo", aliases = ["sinfo"])
    @commands.guild_only()
    async def serverinfo(self, ctx : commands.Context):
        '''Shows Server Info'''
        server = ctx.guild
        roles = str(len(server.roles))
        emojis = str(len(server.emojis))
        channels = str(len(server.channels))

        embed = disnake.Embed(title=server.name, colour=C_MAIN)
        embed.set_thumbnail(url=server.icon.url)
        embed.add_field(name="Server ID:", value=server.id, inline=False)
        embed.add_field(name="Total Users:", value=server.member_count, inline=True)
        embed.add_field(name="Server owner:", value=ctx.guild.owner, inline=True)
        # embed.add_field(name="Server Region:", value=server.region, inline=True)
        embed.add_field(name="Verification Level:", value=server.verification_level, inline=True)
        embed.add_field(name="Role Count:", value=roles, inline=True)
        embed.add_field(name="Emoji Count:", value=emojis, inline=True)
        embed.add_field(name="Channel Count:", value=channels, inline=True)

        await ctx.reply(embed=embed)

    @commands.command(description=f"Shows Server Members.")
    @commands.guild_only()
    async def users(self, ctx):
        '''Shows Server Members'''
        server = ctx.guild
        embed = disnake.Embed(colour=C_MAIN)
        embed.add_field(name="Total Server Members:", value=server.member_count, inline=True)
        return await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))