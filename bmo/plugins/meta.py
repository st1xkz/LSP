import time

import alluka
import hikari
import tanjun

meta = tanjun.Component(name="meta")


@meta.with_slash_command
@tanjun.as_slash_command("ping", "Shows bot's ping/latency")
async def cmd_ping(
    ctx: tanjun.abc.Context, client: alluka.Injected[hikari.GatewayBot]
) -> None:
    start = time.perf_counter()
    message = await ctx.respond(
        f"Pong! 🏓 \n" f"Ws Latency: **{client.heartbeat_latency * 1000:.0f}ms**"
    )
    end = time.perf_counter()

    await ctx.edit_last_response(
        f"Pong! 🏓 \n"
        f"Gateway: **{client.heartbeat_latency * 1000:,.0f}ms**\n"
        f"REST: **{(end-start)*1000:,.0f}ms**"
    )


@meta.with_slash_command
@tanjun.as_slash_command("botinfo", ["bot", "stats"], "Displays info about the bot")
async def cmd_bot(ctx: tanjun.abc.Context) -> None:
    pass


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(meta.copy())
