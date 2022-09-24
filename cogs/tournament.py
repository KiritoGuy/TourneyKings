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

class tournament(commands.Cog):
    """ Commands related to tournament"""
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("tourney Cog Loaded Succesfully")

    async def new_server(self, server_id : int):
            new__server = {"server_id": server_id, "active": "no", "organizer": 0, "registeration_channel": 0, "registeration_category": 0, "registration_time": 0, "confimed_role": 0, "slots": 0}
            await tournament.insert_one(new__server)


    async def new_tournament(self, server_id : int, registeration_channel: int, registeration_category : int, registration_time : 0, confimed_role : int, slots : int):
        if server_id is not None:
            await tournament.update_one({"server_id": server_id}, {"$set": {"registeration_channel": registeration_channel, 
                                                              "registeration_category" : registeration_category, 
                                                              "registration_time" : registration_time, 
                                                              "confimed_role" : confimed_role, 
                                                              "slots" : slots}
                                                    }
                                       )
    async def add_organizer(self, server_id : int, organizers : int)
        if server_id is not None:
            await tournament.update_one({"server_id": server_id}, {"$set": {"organizer": organizers}})



    @app_commands.command(name="start")
    async def my_command(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Hello from command 1!", ephemeral=True)
