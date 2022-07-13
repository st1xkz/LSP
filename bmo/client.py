import os
import hikari
import tanjun
import uvloop

def build_bot() -> GatewayBot:
    TOKEN = os.environ['TOKEN']
    bot = hikari.GatewayBot(TOKEN)

    make_client(bot)

    return bot

def make_client(bot: hikari.GatewayBot) -> tanjun.Client:
    client = (
        tanjun.Client.from_gateway_bot(
            bot,
            mention_prefix=True,
            set_global_commands=993565814517141514
        )
    ).add_prefix(".")

    return client

if os.name != "nt":
    uvloop.install()