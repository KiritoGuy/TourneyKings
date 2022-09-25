from logging import basicConfig, INFO
from config import TOKEN, OWNER_IDS
from utils.bot import TourneyKings
from os import environ
from handler import InteractionClient

basicConfig(level=INFO)

client = TourneyKings()
InteractionClient(client)


environ.setdefault("JISHAKU_HIDE", "1")
environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")


@client.check
async def check_commands(ctx):
    if ctx.guild is None:
        return False
    if ctx.author.bot:
        return False

@client.listen('on_global_commands_update')
async def on_global_commands_update(commands: list):
    print(f'{len(commands)} Global commands updated')


@client.listen('on_guild_commands_update')
async def on_guild_commands_update(commands: list, guild_id: int):
    print(f"{len(commands)} Guild commands updated for guild ID: {guild_id}")


if __name__ == '__main__':
    client.run(TOKEN)
