from __future__ import annotations

import os

import hikari
import tanjun
import uvloop
from dotenv import load_dotenv

from lsp.core import color_logs
from lsp.errors import *

load_dotenv()


class Bot(hikari.GatewayBot):
    def run(self, **kwargs) -> None:

        super().run(
            status=hikari.Status.IDLE,
            activity=hikari.Activity(
                name="Oh, my Glob!", type=hikari.ActivityType.PLAYING
            ),
        )


def build_bot() -> hikari.GatewayBot:
    TOKEN = os.getenv("TOKEN", "")
    return make_client(Bot(TOKEN, banner=None, intents=hikari.Intents.ALL))[1]


def make_client(bot: hikari.GatewayBot) -> tuple[tanjun.Client, hikari.GatewayBot]:
    client = tanjun.Client.from_gateway_bot(
        bot,
        declare_global_commands=True,
    )
    client.load_modules("lsp.components.meta")
    client.load_modules("lsp.components.starboard")
    client.set_hooks(tanjun.AnyHooks().set_on_error(on_error))

    return client, bot


if os.name != "nt":
    uvloop.install()
