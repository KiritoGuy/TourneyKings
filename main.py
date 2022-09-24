from datetime import datetime, timedelta
from os import listdir, system

import aiohttp
import discord
import json

from discord.ext import commands
from pretty_help import PrettyHelp
from config import *


class TourneyKings(commands.Bot): # defining our bot here [ PART 1 ]
    def __init__(self):
        self.description = """Tourney King An Powerful Bot For Sure"""

        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            intents=discord.Intents.all(),
            help_command=PrettyHelp(),
            description=self.description,
            case_insensitive=True,
            start_time=datetime.utcnow(),
        )

    async def on_connnect(self):
        self.session = aiohttp.ClientSession(loop=self.loop)

        cT = datetime.now() + timedelta(
            hours=5, minutes=30
        )  # GMT+05:30 is Our TimeZone So.

        print(
            f"[ Log ] {self.user} Connected at {cT.hour}:{cT.minute}:{cT.second} / {cT.day}-{cT.month}-{cT.year}"
        )

    async def on_ready(self):
        cT = datetime.now() + timedelta(
            hours=5, minutes=30
        )  # GMT+05:30 is Our TimeZone So.

        print(
            f"[ Log ] {self.user} Ready at {cT.hour}:{cT.minute}:{cT.second} / {cT.day}-{cT.month}-{cT.year}"
        )
        print(f"[ Log ] GateWay WebSocket Latency: {self.latency*1000:.1f} ms")

client = TourneyKings() # defining our bot here [ PART 2 ]

with open('./data.json') as f:
  d1 = json.load(f)
with open('./market.json') as f:
  d2 = json.load(f)

def bot_info():
    return d1
def market_info():
    return d2

@client.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Done")


@client.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send("Done")


@client.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Done")


for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

client.load_extension("jishaku")
client.loop.run_until_complete(client.run(TOKEN))
