import os

import hikari
import lavasnek_rs
import tanjun
import uvloop

from bmo.core import color_logs
from bmo.errors import *

LAVALINK_PASSWORD = "bmo"


class EventHandler:
    """Handles events from the Lavalink server."""

    async def track_start(
        self, _: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackStart
    ) -> None:
        """Handles track start events."""
        print(f"Track started on guild: {event.guild_id}")

    async def track_finish(
        self, _: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackFinish
    ) -> None:
        """Handles track finish events."""
        print(f"Track finished on guild: {event.guild_id}")

    async def track_exception(
        self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackException
    ) -> None:
        """Handles track exception events."""
        print(f"Track exception event happened on guild: {event.guild_id}")

        # If a track was unable to be played, skip it
        skip = await lavalink.skip(event.guild_id)
        node = await lavalink.get_guild_node(event.guild_id)

        if skip and node:
            if not node.queue and not node.now_playing:
                await lavalink.stop(event.guild_id)


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
    client.load_modules("bmo.plugins.music")
    client.set_hooks(tanjun.AnyHooks().set_on_error(on_error))

    @client.on_listener(hikari.ShardReadyEvent)
    async def on_shard_ready(
        event: hikari.ShardReadyEvent,
        client_: tanjun.Client = tanjun.Injected(type=tanjun.Client),
    ) -> None:
        """Event that triggers when the hikari gateway is ready."""
        builder = (
            lavasnek_rs.LavalinkBuilder(event.my_user.id, build_bot.bot.TOKEN)
            .set_host("127.0.0.1")
            .set_password(LAVALINK_PASSWORD)
            .set_start_gateway(False)
            # We set start_gateway to False because hikari can handle
            # voice events for us.
        )

        # Here we add lavasnek_rs.Lavalink as a type dependency to the client.
        # We will use this later to have access to it in all of our commands
        client_.set_type_dependency(
            lavasnek_rs.Lavalink, await builder.build(EventHandler)
        )

    @client.with_listener(hikari.VoiceStateUpdateEvent)
    async def on_voice_state_update(
        event: hikari.VoiceStateUpdateEvent,
        lavalink: lavasnek_rs.Lavalink = tanjun.Injected(type=lavasnek_rs.Lavalink),
    ) -> None:
        """Passes voice state updates to Lavalink."""
        lavalink.raw_handle_event_voice_state_update(
            event.state.guild_id,
            event.state.user_id,
            event.state.session_id,
            event.state.channel_id,
        )

    @client.with_listener(hikari.VoiceServerUpdateEvent)
    async def on_voice_server_update(
        event: hikari.VoiceServerUpdateEvent,
        lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
    ) -> None:
        """Passes voice server updates to lavalink."""
        if event.endpoint is not None:
            await lavalink.raw_handle_event_voice_server_update(
                event.guild_id,
                event.endpoint,
                event.token,
            )


if os.name != "nt":
    uvloop.install()
