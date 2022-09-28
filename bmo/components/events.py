import alluka
import hikari
import tanjun

component = tanjun.Component()

# turn this into an event. make into `on_guild_join`
"""
@component.with_listener(hikari.GuildJoinEvent)
async def on_guild_join(event: hikari.GuildJoinEvent, ctx: tanjun.abc.Context, bot: alluka.Injected[hikari.GatewayBot]):
"""


@listener.with_slash_command
@tanjun.as_slash_command("foo", "Bar")
async def cmd_foo(
    ctx: tanjun.abc.Context, bot: alluka.Injected[hikari.GatewayBot]
) -> None:
    bot_user = bot.get_me()

    embed = hikari.Embed(
        title="Beep Boop!",
        description="""Thank you for inviting me! Type `/` to see what I can do!

All configuration is done through `/settings`. If you need any help or support, feel free to contact the [**developer**](https://discord.com/users/690631795473121280).""",
        color=0x3E77EE,
    )
    embed.set_thumbnail(bot_user.avatar_url or bot_user.default_avatar_url)
    await ctx.respond(embed=embed)


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(listener.copy())
