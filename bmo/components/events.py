from __future__ import annotations

import typing as t

import hikari
import tanjun

from bmo.core.tb_errors import CacheFailureError

component = tanjun.Component(name="Component")



def calculate_permissions(
    member: hikari.Member, channel: t.Optional[hikari.GuildChannel] = None
) -> hikari.Permissions:
    guild = member.get_guild()
    if not guild:
        raise CacheFailureError("Guild could not be resolved from cache.")

    if guild.owner_id == member.id:
        return hikari.Permissions.all_permissions()

    guild_roles = guild.get_roles()
    member_roles = list(filter(lambda r: r.id in member.role_ids, guild_roles.values()))
    permissions: hikari.Permissions = guild_roles[
        guild.id
    ].permissions  # Start with @everyone perms

    for role in member_roles:
        permissions |= role.permissions

    if permissions & hikari.Permissions.ADMINISTRATOR:
        return hikari.Permissions.all_permissions()

    if not channel:  # End of role-based permissions
        return permissions

    overwrite_everyone = channel.permission_overwrites.get(channel.guild_id)
    assert overwrite_everyone is not None
    permissions &= ~overwrite_everyone.deny
    permissions |= overwrite_everyone.allow

    overwrites = hikari.PermissionOverwrite(  # Collect role overwrites here
        id=hikari.Snowflake(69),
        type=hikari.PermissionOverwriteType.ROLE,
        allow=hikari.Permissions.NONE,
        deny=hikari.Permissions.NONE,
    )

    for role in member_roles:
        if overwrite := channel.permission_overwrites.get(role.id):
            overwrites.deny |= overwrite.deny
            overwrites.allow |= overwrite.allow

    permissions &= ~overwrites.deny
    permissions |= overwrites.allow

    if overwrite_member := channel.permission_overwrites.get(member.id):
        permissions &= ~overwrite_member.deny
        permissions |= overwrite_member.allow

    return permissions


@component.with_listener(hikari.GuildJoinEvent)
async def on_guild_join(event: hikari.GuildJoinEvent):
    guild = event.get_guild()
    bot_user = event.app.get_me()

    for _, ch in guild.get_channels().items():
        if calculate_permissions(bot_user, ch) & hikari.Permissions.SEND_MESSAGES:
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
