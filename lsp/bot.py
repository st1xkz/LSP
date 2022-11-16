import os

import aiohttp
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


bot.load_extensions_from("./lsp/plugins/", must_exist=True)


if os.name != "nt":
    uvloop.install()
