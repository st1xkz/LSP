import hikari
import tanjun

settings = tanjun.Component()


@settings.with_slash_command
@tanjun.with_user_slash_option("obj", "Object to get help for", default=False)
@tanjun.as_slash_command("settings", "Configure different settings of the bot")
async def cmd_ping(ctx: tanjun.abc.Context, obj: str) -> None:
    if not obj:
        embed = hikari.Embed(
            title="DJ BMO ~ Settings",
            description="To view more info about an option, use `/settings <obj>`.",
        )
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("make sure this works properly")


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(settings.copy())
