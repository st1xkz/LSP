import tanjun
import time

component = tanjun.Component()


@component.with_slash_command
@tanjun.as_slash_command(name="ping", description="Shows the bot's ping/latency")
async def cmd_ping(ctx: tanjun.abc.Context) -> None:
    start = time.perf_counter()
    message = await ctx.respond(
        f"Pong! 🏓 \n"
        f"Ws Latency: **{ctx.client.heartbeat_latency * 1000:.0f}ms**"
    )
    end = time.perf_counter()

    await message.edit(
        f"Pong! 🏓 \n"
        f"Gateway: **{ctx.client.heartbeat_latency * 1000:,.0f}ms**\n"
        f"REST: **{(end-start)*1000:,.0f}ms**"
    )


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
