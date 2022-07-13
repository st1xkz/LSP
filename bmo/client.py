import os

import hikari
import tanjun
import uvloop


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
                mention_prefix=True,
                set_global_commands=[993565814517141514, 870013765071028285],
            )
        )
        .add_prefix(".")
        .load_modules("plugins.utilities")
    )

    return client


if os.name != "nt":
    uvloop.install()
