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
    banner="lsp",
    ignore_bots=True,
    intents=hikari.Intents.ALL,
)


@bot.listen()
async def on_star_starting(event: hikari.StartingEvent) -> None:
    bot.d.star_pool = await asyncpg.create_pool(os.environ.get("PGSQL_HOST"))
    bot.d.aio_star_session = aiohttp.ClientSession()

    await bot.d.star_pool.execute(
        """
        CREATE TABLE IF NOT EXISTS star (
            og_msg_id BIGINT,
            msg_id BIGINT,
            ch_id BIGINT
        );
        """
    )


@bot.listen()
async def on_star_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.aio_star_session.close()


bot.load_extensions_from("./lsp/plugins/", must_exist=True)


if os.name != "nt":
    uvloop.install()
