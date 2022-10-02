import asyncio
import os

import hikari
import tanjun
import uvloop
from dotenv import load_dotenv

from bmo.core import color_logs
from bmo.errors import *

load_dotenv()


def build_bot() -> hikari.GatewayBot:
    TOKEN = os.getenv("TOKEN")
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
        declare_global_commands=True,
    )
    client.load_modules("bmo.components.events")
    client.load_modules("bmo.components.meta")
    client.load_modules("bmo.components.settings")
    client.set_hooks(tanjun.AnyHooks().set_on_error(on_error))

    return client


component = tanjun.Component()


@component.with_listener()
async def on_started(event: hikari.StartedEvent):
    update_presence.start()


@component.with_schedule
@tanjun.as_interval(60)
async def update_presence() -> None:
    await build_bot.update_presence(
        activity=hikari.Activity(
            name="I think I am dying. But that's okay, BMO always bounces back!",
            type=hikari.ActivityType.PLAYING,
        )
    )
    await asyncio.sleep(60)
    await build_bot.update_presence(
        activity=hikari.Activity(
            name=f"{len(component.cache.get_available_guilds_view())} guilds & {len(component.cache.get_users_view())} users!",
            type=hikari.ActivityType.WATCHING,
        )
    )


if os.name != "nt":
    uvloop.install()
