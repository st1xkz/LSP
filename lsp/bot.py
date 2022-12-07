import os

import aiohttp
import asyncpg
import hikari
import lightbulb
import uvloop
from dotenv import load_dotenv

from lsp.core import color_logs
from lsp.errors import *

load_dotenv()


bot = lightbulb.BotApp(
    token=os.getenv("TOKEN"),
    banner=None,
    ignore_bots=True,
    intents=hikari.Intents.ALL,
)


@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.aio_session = aiohttp.ClientSession()


@bot.listen()
async def startup_hook(event: hikari.StartingEvent) -> None:
    # Create database pool
    bot.db_pool: asyncpg.Pool = await asyncpg.create_pool(
        host=os.getenv("SQL_HOST"), max_size=5, min_size=5
    )

    async with bot.db_pool.acquire() as con:
        await con.execute(
            """
            CREATE TABLE IF NOT EXISTS star (
                id INT,
                msg_id INT,
                ch_id INT
            );
            """
        )
        # Create a connection server if needed
        async with con.cursor() as cursor:
            await cursor.fetch("Fetch query...")


bot.load_extensions_from("./lsp/plugins/", must_exist=True)


if os.name != "nt":
    uvloop.install()
