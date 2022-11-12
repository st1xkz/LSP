import datetime as dt
import inspect
import os
import platform
import time
from datetime import datetime, timedelta

import hikari
import lightbulb
from psutil import Process, virtual_memory  # type: ignore

from lsp.core import chron

meta = lightbulb.Plugin("meta")


@meta.command
@lightbulb.command(
    name="ping",
    description="Shows bot's ping/latency",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    start = time.perf_counter()
    message = await ctx.respond(
        f"Pong! 🏓 \n" f"Ws Latency: **{ctx.bot.heartbeat_latency * 1000:.0f}ms**"
    )
    end = time.perf_counter()

    await message.edit(
        f"Pong! 🏓 \n"
        f"Gateway: **{ctx.bot.heartbeat_latency * 1000:,.0f}ms**\n"
        f"REST: **{(end-start)*1000:,.0f}ms**"
    )


@meta.command
@lightbulb.command(
    name="stats",
    description="Displays info about the bot",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def stats(ctx: lightbulb.Context) -> None:
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
        bot_user = ctx.bot.get_me()

        embed = (
            hikari.Embed(
                title="Statistics for Lumpy Space Princess",
                description=f"""Guild Count: **{len(ctx.bot.cache.get_available_guilds_view())}**
User Count: **{len(ctx.bot.cache.get_users_view())}**
Command Count: **{len(ctx.bot.slash_commands)}**

Uptime: **{uptime}**
CPU Time: **{cpu_time}**
Memory Usage: **{mem_usage:,.3f}/{mem_total:,.0f} MiB ({mem_of_total:,.0f}%)**

Language: **Python**
Python Version: **v{platform.python_version()}**
Library: **hikari-py v{hikari.__version__}**
Command Handler: **hikari-lightbulb v{lightbulb.__version__}**""",
                color=0xB87FDE,
                timestamp=datetime.now().astimezone(),
            )
            .set_thumbnail(
                bot_user.avatar_url or bot_user.default_avatar_url,
            )
            .set_footer(text=f"Bot developed by sticks#5822")
        )
        await ctx.respond(embed=embed)


@meta.command
@lightbulb.option(
    name="cmd",
    description="the command to get the source for",
    type=str,
    required=False,
)
@lightbulb.command(
    name="source",
    description="Displays link to the bot's GitHub or to a specific command",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def source(ctx: lightbulb.Context, cmd: str) -> None:
    _cmd = ctx.bot.get_slash_command(cmd)
    source_url = "https://github.com/st1xkz/LSP"
    branch = "main"

    with open("./LICENSE") as f:
        license_ = f.readline().strip()
        if not _cmd:
            await ctx.respond(f"<{source_url}>")
            return

        else:
            obj = ctx.bot.get_slash_command(cmd.replace(".", " "))
            if obj is None:
                return await ctx.respond(f"Could not find command called `{_cmd}`.")

            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename

        lines, firstlineno = inspect.getsourcelines(src)
        if not module.startswith("discord"):
            if filename is None:
                return await ctx.respond(f"Could not find source for command `{_cmd}`.")

            location = os.path.relpath(filename).replace("\\", "/")
        else:
            location = module.replace(".", "/") + ".py"

        await ctx.respond(
            f"<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>"
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(meta)
