import datetime as dt
import inspect
import os
import platform
import time
from datetime import datetime, timedelta

import alluka
import hikari
import tanjun
from psutil import Process, virtual_memory  # type: ignore

from lsp.core import chron

meta = tanjun.Component()


@meta.with_slash_command
@tanjun.as_slash_command("ping", "Shows bot's ping/latency")
async def ping(
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
@tanjun.as_slash_command("stats", "Displays info about the bot")
async def stats(
    ctx: tanjun.abc.Context,
    bot: alluka.Injected[hikari.GatewayBot],
    client: alluka.Injected[tanjun.abc.Client],
) -> None:
    if not (guild := ctx.get_guild()):
        return

    if not (me := guild.get_my_member()):
        return

    if not (member := ctx.member):
        return

    with (proc := Process()).oneshot():
        uptime = chron.short_delta(
            dt.timedelta(seconds=time.time() - proc.create_time())
        )
        cpu_time = chron.short_delta(
            dt.timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user),
            ms=True,
        )
        mem_total = virtual_memory().total / (1024**2)
        mem_of_total = proc.memory_percent()
        mem_usage = mem_total * (mem_of_total / 100)
        assert (bot_user := bot.get_me())
        assert ctx.cache
        embed = (
            hikari.Embed(
                title="Statistics for Lumpy Space Princess",
                description=f"""Guild Count: **{len(ctx.cache.get_available_guilds_view())}**
User Count: **{len(ctx.cache.get_users_view())}**
Command Count: **{sum(1 for _ in client.iter_slash_commands())}**

Uptime: **{uptime}**
CPU Time: **{cpu_time}**
Memory Usage: **{mem_usage:,.3f}/{mem_total:,.0f} MiB ({mem_of_total:,.0f}%)**

Language: **Python**
Python Version: **v{platform.python_version()}**
Library: **hikari-py v{hikari.__version__}**
Command Handler: **hikari-tanjun v{tanjun.__version__}**""",
                color=0xB87FDE,
                timestamp=datetime.now().astimezone(),
            )
            .set_thumbnail(
                bot_user.avatar_url or bot_user.default_avatar_url,
            )
            .set_footer(text=f"Bot developed by sticks#5822")
        )
        await ctx.respond(embed=embed)


@meta.with_slash_command
@tanjun.with_str_slash_option("cmd", "the command to get the source for", default=None)
@tanjun.as_slash_command(
    "source",
    "Displays link to the bot's GitHub or to a specific command",
)
async def source(ctx: tanjun.abc.Context, cmd: str) -> None:
    source_url = "https://github.com/st1xkz/LSP"
    branch = "main"

    if cmd is None:
        await ctx.respond(f"<{source_url}>")
        return
    else:
        try:
            _cmd: tanjun.abc.BaseSlashCommand | None = None
            for command in ctx.client.iter_slash_commands():
                if command.name == cmd:
                    _cmd = command
                    break
            assert _cmd is not None and isinstance(_cmd, tanjun.SlashCommand)
        except AssertionError:
            await ctx.respond(f"Could not find command called `{cmd}`.")
            return None

        src = _cmd.callback.__code__
        module = _cmd.callback.__module__
        filename = src.co_filename

    lines, firstlineno = inspect.getsourcelines(src)
    if not module.startswith("discord"):
        if filename is None:
            await ctx.respond(f"Could not find source for command `{_cmd.name}`.")
            return

        location = os.path.relpath(filename).replace("\\", "/")
    else:
        location = module.replace(".", "/") + ".py"

    await ctx.respond(
        f"<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>"
    )


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(meta.copy())
