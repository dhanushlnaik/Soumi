import disnake
from disnake.ext import commands
from database import guild

def modEmbed(action):
    emb = disnake.Embed(color=0xf72585)
    emb.set_author(name=action)
    return emb

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "꒰ <a:ModerationCategory:943428021212307476> ꒱"
        self.hidden = False
        self.description = "Includes M<oderation Related Commands."

    @commands.command(usage=f"`< amount >`", description=f"Purge Messages.")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def clear(self, ctx, amount = 0):
        '''Purge Messages'''
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(embed = modEmbed(f'Deleted {amount} messages'))

    @commands.command(usage=f"`< member >` `[ reason ]`", description=f"Kick a Member.")
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member : disnake.Member, *, reason=None):
        '''Kick a Member'''
        await ctx.message.delete()
        await member.kick(reason=reason)
        await ctx.send(embed = modEmbed(f':hammer: {member.mention} has been kicked.'))

    @commands.command(usage=f"`< member >` `[ reason ]`", description=f"Ban a Member.")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member : disnake.Member, *, reason=None):
        '''Ban a Member'''
        await ctx.message.delete()
        await member.ban(reason=reason)
        await ctx.send(embed=modEmbed(f':hammer: {member.mention} has been banned.'))

    @commands.command(usage=f"`< member >` `[ reason ]`", description=f"Unban a Member.")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, *,member):
        '''Unban a Member'''
        await ctx.message.delete()
        banned_users = await ctx.guild.bans()

        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(embed = modEmbed(f'{user.mention} has been unbanned.'))

    @commands.command(aliases=["nick"], usage=f"`< member >` `[ reason ]`", description=f"Change Nickname of a member.")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: disnake.Member, *, name: str = None):
        '''Change Nickname of a member.'''
        await member.edit(nick=name)
        message = f"Changed {member.mention}'s nickname to **{name}**"
        if name is None:
            message = f"Reset {member.mention}'s nickname"
        await ctx.reply(embed = modEmbed(message))

    @commands.command(usage=f"`< member >` `[ reason ]`", description=f"Mute a member.")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    async def mute(self, ctx, member: disnake.Member, *, reason: str = None):
        '''Mute a member'''
        muted_role = next((g for g in ctx.guild.roles if g.name == "Muted"), None)
        if not muted_role:
            return await ctx.send(embed = modEmbed("There is no role called **Muted**"))
        try:
            await member.add_roles(muted_role, reason=reason)
            await ctx.send(embed = modEmbed(f"{member.mention} has been muted."))
        except Exception as e:
            await ctx.send(embed = modEmbed(e))

    @commands.command(usage=f"`< member >` `[ reason ]`", description=f"Unmute a Member.")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    async def unmute(self, ctx, member: disnake.Member, *, reason: str = None):
        '''Unmute a Member'''
        muted_role = next((g for g in ctx.guild.roles if g.name == "Muted"), None)
        if not muted_role:
            return await ctx.send(embed = modEmbed("There is no role called **Muted**"))
        try:
            await member.remove_roles(muted_role, reason=reason)
            await ctx.send(embed = modEmbed(f"{member.mention} has been unmuted."))
        except Exception as e:
            print(e)
    
    @commands.command(description=f"Move Every Member in VC.")
    @commands.guild_only()
    @commands.has_guild_permissions(move_members=True)
    async def voicemove(self, ctx):
        '''Move Every Member in VC'''
        voiceClient = disnake.utils.get(self.bot.voice_clients, guild = ctx.guild)
        
        if voiceClient != None:
            if len(voiceClient.channel.members) == 1:
                await voiceClient.disconnect() # Disconnect
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            return await ctx.send("Connect to a voice channel!")
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        await ctx.author.voice.channel.connect()
        await ctx.send(embed = modEmbed("Move me to Move all The Members in VC!"))


    # @commands.Cog.listener()
    # async def on_voice_state_update(self,member, before, after):
        # if not member == self.bot.user:
        #     return
        # if after.channel == None or before.channel == None:
        #     return
        # channel = self.bot.get_channel(before.channel.id)
        # members = channel.members
        # memids= []
        # for member in members:
        #     memids.append(member.id)
        #     await member.move_to(after.channel)
            
        # voiceClient = disnake.utils.get(self.bot.voice_clients, guild = member.guild)
        # if voiceClient.channel != None:
        #     if len(voiceClient.channel.members) == 1:
        #         await voiceClient.disconnect() # Disconnect 939453610151014440
        # if not member == self.bot.user:
        #     return
        # if after.channel == None or before.channel == None:
        #     return

    @commands.command(aliases=['pre', 'setprefix', 'change_prefix'], brief="Get or set the command prefix for this server.",usage="`< new prefix >`",help="", extras={"emoji": "🔧"},description="Get or set the command prefix for this server.")
    @commands.guild_only()
    async def prefix(self, ctx, newpre:str=None):
        if newpre is None:
            emb = disnake.Embed(color=0x1cbaff)
            emb.set_author(name=f"My prefix is  `{guild.check_prefix(ctx.guild.id)}`")
            await ctx.channel.send(embed=emb)
            return
        else: 
            if ctx.message.author.guild_permissions.administrator:
                guild.add_prefix(ctx.guild.id, newpre)
                emb = disnake.Embed(color=disnake.Color.green())
                emb.set_author(name=f"✅ Changed server prefix to `{guild.check_prefix(ctx.guild.id)}`")
                await ctx.channel.send(embed=emb)
                return
            else:
                emb = disnake.Embed(color=disnake.Color.red())
                emb.set_author(name=f"❌ You don't have required Permissions to use this Command!")
                await ctx.channel.send(embed=emb)
                return 

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(move_members=True)
    async def voicerole(self, ctx, role:disnake.Role):
        
        voiceClient = disnake.utils.get(self.bot.voice_clients, guild = ctx.guild)
        
        if voiceClient != None:
            if len(voiceClient.channel.members) == 1:
                await voiceClient.disconnect() # Disconnect
        channel = ctx.author.voice.channel
        if channel is None:
            return await ctx.send("Connect to a voice channel!")
        members = channel.members
        for member in members:
            await member.add_roles(role)
        await ctx.channel.send("DOone")


def setup(bot):
    bot.add_cog(Moderation(bot))