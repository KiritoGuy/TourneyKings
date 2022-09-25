import motor.motor_asyncio as motor
import time
import os
import re
import discord
import aiohttp
import sys
import traceback

from config import (
    TOKEN, DATABASE_URL, DB_UPDATE_INTERVAL
)

class TourneyKings(commands.AutoShardedBot):
    def __init__(self):
        self.app_cmds: dict = {}
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(
            command_prefix=TourneyKings.get_custom_prefix,
            intents=intents,
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions.none(),
            strip_after_prefix=True,
            help_command=TourneyKingHelp(),
            cached_messages=10000,
            owner_ids = OWNERS,
            activity=discord.Activity(type=discord.Streaming, name="kirito is doing some weird shit rn", url="https://twitch.com/quantumgamer7"),
        )
        cluster = motor.AsyncIOMotorClient(DATABASE_URL)
        self.session = aiohttp.ClientSession()

        self.cache_loaded = False
        self.cogs_loaded = False
        self.views_loaded = False

        self.last_updated_prefixes_db = 0
        self.last_updated_user_profile_db = 0
        self.last_updated_serverconfig_db = 0
        self.last_updated_global_db = 0

        self.db = cluster['TourneyKings']
        
        self.prefixes = self.db['prefixes']
        self.user_profile_db = self.db['user_profile']
        self.serverconfig = self.db['serverconfig']
        self.global_db = self.db['global']
        self.blacklisted = self.db['blacklisted']

        self.prefixes_cache = []
        self.blacklisted_cache = []
        self.serverconfig_cache = []
        self.global_cache = []
        self.user_profile_cache = []

        self.update_prefixes_db.start()
        self.update_serverconfig_db.start()
        self.update_global_db.start()
        self.update_user_profile_db.start()

        if not self.cache_loaded:
            self.loop.run_until_complete(self.get_cache())
            self.loop.run_until_complete(self.get_blacklisted_users())
            self.cache_loaded = True

        if not self.cogs_loaded:
            self.load_extension('jishaku')
            print("Loaded jsk!")
            self.loaded, self.not_loaded = self.loop.run_until_complete(self.load_extensions('./cogs'))
            self.loaded_hidden, self.not_loaded_hidden = self.loop.run_until_complete(self.load_extensions('./cogs_hidden'))
            self.cogs_loaded = True

    async def set_default_guild_config(self, guild_id):
        pain = {
            "_id": guild_id,
            "tourney": {"active": None, "game": None, "count": None, "slots": 0, "Name": None, "reg_category": None, "reg_channel": None, "reg_time": None, "confimed_role": None, "reg_message": 0},
        }

        self.serverconfig_cache.append(pain)
        return await self.get_guild_config(guild_id)

    async def get_guild_config(self, guild_id):
        for e in self.serverconfig_cache:
            if e['_id'] == guild_id:
                if "tourney" not in e:
                    e.update({"tournament": {"active": None, "game": None, "count": None, "slots": 0, "name": None, "reg_catagory": None, "reg_channel": None, "reg_time": None, "confimed_role": None, "reg_message": 0}})
                return e
        return await self.set_default_guild_config(guild_id)

    @tasks.loop(seconds=DB_UPDATE_INTERVAL, reconnect=True)
    async def update_prefixes_db(self):
        if self.cache_loaded:
            cancer = []
            for e in self.prefixes_cache:
                hmm = UpdateOne(
                    {"_id": e["_id"]},
                    {"$set": {"prefix": e['prefix']}},
                    upsert=True
                )
                cancer.append(hmm)
            if len(cancer) != 0:
                await self.prefixes.bulk_write(cancer)
            self.last_updated_prefixes_db = time.time()


    @tasks.loop(seconds=DB_UPDATE_INTERVAL, reconnect=true)
    async def update_user_profile_db(self):
        if self.cache_loaded:
            cancer = []
            for h in self.user_profile_cache:
                hh = h.copy()
                hh.pop("_id")
                hmm = updateone(
                    {"_id": h["_id"]},
                    {"$set": hh},
                    upsert=true
                )
                cancer.append(hmm)
            if len(cancer) != 0:
                await self.user_profile_db.bulk_write(cancer)
            self.last_updated_user_profile_db = time.time()
