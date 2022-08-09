import hikari
import tanjun

help = tanjun.Component(name="help")

@help.with_slash_command
@tanjun.as_slash_command("help", "Shows help about all or one specific command")
async def custom_help(ctx: tanjun.abc.Context) -> None:
    await ctx.respond("this is help")

@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(help.copy())