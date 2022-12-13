from datetime import datetime

import asyncpg
import hikari
import lightbulb

starboard = lightbulb.Plugin("starboard")

emoji = "⭐"
min_reaction = 1  # Minimum reactions required to add the message to starboard


@starboard.listener(hikari.GuildReactionAddEvent)
async def reaction_added(event: hikari.GuildReactionAddEvent) -> None:
    if not event.is_for_emoji("⭐"):
        return

    message = await starboard.bot.rest.fetch_message(event.channel_id, event.message_id)
    num_reaction = (
        [
            reaction
            for reaction in message.reactions
            if str(reaction.emoji.name) == event.emoji_name
        ][0]
    ).count
    jump_url = f"https://discord.com/channels/{message.guild_id}/{message.channel_id}/{message.id}"

    if num_reaction == min_reaction:
        embed = hikari.Embed(
            title=f"Jump to message in #{starboard.bot.cache.get_guild_channel(message.channel_id).name}",
            url=jump_url,
            color=0xFFEA00,
            timestamp=datetime.now().astimezone(),
        )
        embed.set_author(
            name=f"{message.author}",
            icon=message.author.avatar_url or message.author.default_avatar_url,
        )
        embed.set_footer(text=f"ID: {message.id}")
        if message.attachments:
            # Check if attachment is an image
            embed.set_image(message.attachments[0].url)
        if message.content:
            embed.description = message.content

        async with event.app.d.db_pool.acquire() as con:
            msg = await starboard.bot.rest.create_message(
                1035754257686728734, f"⭐ {num_reaction}", embed=embed
            )
            await con.execute(
                "INSERT INTO star VALUES ($1, $2, $3)",
                event.message_id,
                msg.id,
                msg.channel_id,
            )
    if num_reaction > min_reaction:
        async with event.app.d.db_pool.acquire() as con:
            con: asyncpg.connection.Connection
            data = await con.fetchrow(
                "SELECT * FROM star WHERE og_msg_id = $1", event.message_id
            )
            if not data:
                return
            await starboard.bot.rest.edit_message(
                data.get("ch_id"), data.get("msg_id"), content=f"⭐ {num_reaction}"
            )


@starboard.listener(hikari.GuildReactionDeleteEvent)
async def reaction_removed(event: hikari.GuildReactionDeleteEvent) -> None:
    if not event.is_for_emoji("⭐"):
        return

    message = await starboard.bot.rest.fetch_message(event.channel_id, event.message_id)
    num_reaction = (
        [
            reaction
            for reaction in message.reactions
            if str(reaction.emoji.name) == event.emoji_name
        ][0]
    ).count
    jump_url = f"https://discord.com/channels/{message.guild_id}/{message.channel_id}/{message_id}"

    if num_reaction >= min_reaction:
        async with evet.app.d.db_pool.acquire() as con:
            con: asyncpg.connection.Connection
            data = await con.fetchrow(
                "SELECT * FROM star WHERE og_msg_id = $1", event.message_id
            )
            if not data:
                return
            await starboard.bot.rest.edit_message(
                data.get("ch_id"), data.get("msg_id"), content=f"⭐ {num_reaction}"
            )

    else:
        async with event.app.d.db_pool.acquire() as con:
            con: asyncpg.connection.Connection
            data = await con.fetchrow(
                "SELECT * FROM star WHERE og_msg_id = $1", event.message_id
            )
            if not data:
                return
            await starboard.bot.rest.delete_message(
                data.get("ch_id"), data.get("msg_id")
            )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(starboard)
