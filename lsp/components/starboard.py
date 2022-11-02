import hikari
import tanjun
import toolbox

starboard = tanjun.Component()


@starboard.with_listener(hikari.GuildJoinEvent)
async def on_guild_join(event: hikari.GuildJoinEvent):
    assert (member := event.guild.get_my_member())
    assert (ch := event.guild.get_channel(event.guild.system_channel_id))  # type: ignore

    if toolbox.calculate_permissions(member, ch) & hikari.Permissions.SEND_MESSAGES:
        await event.app.rest.create_message(
            ch.id,
            embed=hikari.Embed(
                title="Beep Boop!",
                description="""Thank you for inviting me! Type `/` to see what I can do!
                
All configuration is done through `/settings`. If you need any help or support, feel free to contact the [**developer**](https://discord.com/users/690631795473121280).""",
                color=0x3E77EE,
            ).set_thumbnail(member.avatar_url or member.default_avatar_url),
        )


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(starboard.copy())