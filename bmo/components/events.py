import hikari
import tanjun

component = tanjun.Component(name="Component")


@component.with_listener(hikari.GuildJoinEvent)
async def on_guild_join(event: hikari.GuildJoinEvent):
    guild = event.get_guild()
    bot_user = event.app.get_me()

    for _, ch in guild.get_channels().items():
        if toolbox.calculate_permissions(member, ch) & hikari.Permissions.SEND_MESSAGES:
            await event.client.rest.create_message(
                ch,
                embed=hikari.Embed(
                    title="Beep Boop!",
                    description="""Thank you for inviting me! Type `/` to see what I can do!
                    
All configuration is done through `/settings`. If you need any help or support, feel free to contact the [**developer**](https://discord.com/users/690631795473121280).""",
                    color=0x3E77EE,
                ).set_thumbnail(bot_user.avatar_url or bot_user.default_avatar_url),
            )
        break


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
