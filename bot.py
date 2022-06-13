import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv
import constants as var
from database import user, guild
import traceback
import asyncio
import random
from simple_chalk import chalk 
import datetime
from constants import C_INVISIBLE , C_MAIN

load_dotenv()
# TOKEN = os.environ.get("TOKEN")

DEFAULT_PREFIX = var.DEFAULT_PREFIX


async def prefix_get(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)
    prefix = guild.check_prefix(message.guild.id)
    return commands.when_mentioned_or(prefix, DEFAULT_PREFIX)(bot, message)

async def switchpresence():
    await bot.wait_until_ready()
    statuses = ["UR MOM"]
    while not bot.is_closed():
        status = random.choice(statuses)
        await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing, name=status))
        await asyncio.sleep(10)

def unload_cogs():
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            try:
                bot.unload_extension(f"cogs.{file[:-3]}")
            except Exception as e:
                print(f"COG UNLOAD ERROR : {e}")

def load_cogs():
    print("Loading...")
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and not file.startswith("_"):
             
            try:
                bot.load_extension(f"cogs.{file[:-3]}")
                print(f'> Loaded cog: {file[:-3]}'.title())
            except Exception as e:
                print(f"COG LOAD ERROR : {e}\n\n{traceback.format_exc()}\n\n")


intents = disnake.Intents().all()
bot = commands.Bot(command_prefix=prefix_get, help_command=None, intents=intents)


@bot.command(aliases=["reload"], hidden=True)
@commands.is_owner()
async def reloadcogs(ctx):
    unload_cogs()
    load_cogs()
    embed = disnake.Embed(description="All Cogs Reloaded !" , color=var.C_INVISIBLE)
    await ctx.reply(embed=embed)


@bot.event
async def on_ready():
    print(chalk.green(f"🔵 | Logged in as : {bot.user.name}\nID : {bot.user.id}"))
    load_cogs()
    if not hasattr(bot, "uptime"):
        bot.uptime = datetime.datetime.now()
    print(chalk.green(f"Ready: {bot.user} | Servers: {len(bot.guilds)}"))

@bot.event
async def on_guild_remove(guild):

    bot_count = len([b for b in guild.members if b.bot])
    embed = disnake.Embed(
        title="I just got removed from a server",
        description=guild.name,
        color=var.C_RED
    ).add_field(
        name="ID", value=guild.id, inline=False
    ).add_field(
        name="Member count", value=guild.member_count, inline=False
    ).add_field(
        name="Bot to human percentage", value=f"{round(bot_count / guild.member_count * 100, 2)}%", inline=False
    )

    await bot.get_channel(985561890606444564).send(embed=embed)

bot.loop.create_task(switchpresence())
bot.run("OTgwMDE4NjY1MjY3Mjk4MzI1.GK1_qY.mJ5Mglf62N3flW63L-Jc0CqncWxLFvGxKDTXdU")