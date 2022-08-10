import hikari
import tanjun

help = tanjun.Component(name="help")


@help.with_slash_command
@tanjun.with_str_slash_option("obj", "Object to get help for", default=False)
@tanjun.as_slash_command("help", "Shows help about all or one specific command")
async def custom_help(ctx: tanjun.abc.Context, obj: str) -> None:
    if not obj:
        embed = hikari.Embed(
            description="""Welcome to DJ BMO's help!
Find all the commands available on this panel.""",
            color=0x77F2F2,
        )
        await ctx.respond(embed)


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(help.copy())
