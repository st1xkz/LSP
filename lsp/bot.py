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

    # Create database pool
    bot.d.db_pool: asyncpg.Pool = await asyncpg.create_pool(
        os.getenv("SQL_HOST"), max_size=4, min_size=4
    )

    async with bot.d.db_pool.acquire() as con:
        await con.execute(
            """
            CREATE TABLE IF NOT EXISTS star (
                msg_id BIGINT,
                ch_id BIGINT
            );
            """
        )


bot.load_extensions_from("./lsp/plugins/", must_exist=True)


if os.name != "nt":
    uvloop.install()

