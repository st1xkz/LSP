import os

import hikari
import tanjun
import uvloop
from dotenv import load_dotenv

from lsp.core import color_logs
from lsp.errors import *

load_dotenv()


def build_bot() -> hikari.GatewayBot:
    TOKEN = os.getenv("TOKEN")
    bot = hikari.GatewayBot(
        TOKEN,
        banner=None,
        intents=hikari.Intents.ALL,
    )

    return bot


def make_client(bot: hikari.GatewayBot) -> tanjun.Client:
    client = tanjun.Client.from_gateway_bot(
        bot,
        declare_global_commands=True,
    )
    client.load_modules("lsp.components.meta")
    client.load_modules("lsp.components.starboard")
    client.set_hooks(tanjun.AnyHooks().set_on_error(on_error))

    return client


if os.name != "nt":
    uvloop.install()
