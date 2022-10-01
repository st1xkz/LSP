import hikari
import tanjun
import toolbox

component = tanjun.Component(name="Component")


@component.with_listener(hikari.GuildJoinEvent)
async def on_guild_join(event: hikari.GuildJoinEvent):
    member = event.get_guild().get_my_member()
    ch = event.get_guild().get_channel(event.get_guild().system_channel_id)

    if toolbox.calculate_permissions(member, ch) & hikari.Permissions.SEND_MESSAGES:
        await event.app.rest.create_message(
            ch,
            embed=hikari.Embed(
                title="Beep Boop!",
                description="""Thank you for inviting me! Type `/` to see what I can do!
                
All configuration is done through `/settings`. If you need any help or support, feel free to contact the [**developer**](https://discord.com/users/690631795473121280).""",
                color=0x3E77EE,
            ).set_thumbnail(member.avatar_url or member.default_avatar_url),
        )


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
