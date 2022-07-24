import os

import hikari
import tanjun
import uvloop

from bmo.core import color_logs
from bmo.errors import *


def build_bot() -> hikari.GatewayBot:
    TOKEN = os.environ["TOKEN"]
    bot = hikari.GatewayBot(
        TOKEN,
        banner=None,
        intents=hikari.Intents.ALL,
    )

    make_client(bot)

    return bot


def make_client(bot: hikari.GatewayBot) -> tanjun.Client:
    client = tanjun.Client.from_gateway_bot(
        bot,
    )
    client.load_modules("bmo.plugins.meta")
    client.set_hooks(tanjun.AnyHooks().set_on_error(on_error))

    return client


if os.name != "nt":
    uvloop.install()
