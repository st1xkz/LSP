import alluka
import hikari
import tanjun

from bmo.core import chron

help = tanjun.Component(name="Help")


@help.with_slash_command
@tanjun.with_str_slash_option("obj", "Object to get help for", default=False)
@tanjun.as_slash_command("help", "Shows help about all or one specific command")
async def custom_help(
    ctx: tanjun.abc.Context,
    obj: str,
    bot: alluka.Injected[hikari.GatewayBot],
) -> None:
    bot_user = bot.get_me()
    cd = chron.short_date_and_time(bot_user.created_at)

    info = {}
    for component in ctx.client.components:
        if component.name.lower() == "help":
            continue
        cmds = ctx.client.component.iter_commands()
        info[component] = ", ".join([cmd.name for cmd in cmds])

    if not obj:
        embed = hikari.Embed(
            description="""Welcome to DJ BMO's help!
Find all the commands available on this panel.""",
            color=0x77F2F2,
        )
        for component, cmds in info.items():
            embed.add_field(name=f"{component.name}", value=f"`{cmds}`", inline=False)
        embed.set_author(
            name="DJ BMO • Help",
            icon=bot_user.avatar_url or bot_user.default_avatar_url,
        )
        embed.set_thumbnail(bot_user.avatar_url or bot_user.default_avatar_url)
        embed.set_footer(
            text=f"DJ BMO was created {cd}",
            icon=bot_user.avatar_url or bot_user.default_avatar_url,
        )
        await ctx.respond(embed=embed)



@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(help.copy())
