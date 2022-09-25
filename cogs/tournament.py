import os
import discord
import psutil
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import motor.motor_asyncio
import nest_asyncio
import json
import random
from config import DATABASE_URL
nest_asyncio.apply()

database = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
tournament = database["TOURNEYKING"]["SERVER"]

class Info(commands.Cog):
    """ Commands related to info"""
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("info Cog Loaded Succesfully")


def setup(client):
    client.add_cog(Info(client))
