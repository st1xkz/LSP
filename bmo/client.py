import os

import hikari
import tanjun
import uvloop

from bmo.core import color_logs


def build_bot() -> hikari.GatewayBot:
    TOKEN = os.environ["TOKEN"]
    bot = hikari.GatewayBot(TOKEN)

    make_client(bot)

    return bot


def make_client(bot: hikari.GatewayBot) -> tanjun.Client:
    client = (
        (
            tanjun.Client.from_gateway_bot(
                bot,
                banner=None,
                set_global_commands=[993565814517141514, 870013765071028285],
            )
        )
        .load_modules("bmo.plugins.meta")
    )

    return client


if os.name != "nt":
    uvloop.install()
