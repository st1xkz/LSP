import hikari
import lightbulb

starboard = lightbulb.Plugin("starboard")

emoji = "\u2b50"
min_reaction = 1  # Minimum reactions required to add the message to starboard


@starboard.listener(hikari.GuildReactionAddEvent)
async def reaction_added(event: hikari.GuildReactionAddEvent) -> None:
    # Make sure the bot is listening to events
    print(event.emoji_name)
    if not starboard.bot.is_alive:
        return
    if not str(event.emoji_name) == "\u2b50":
        return

    message = starboard.bot.cache.get_message(
        event.message_id
    ) or await starboard.bot.rest.fetch_message(event.guild_id, event.message_id)
    num_reaction = (
        [
            reaction
            for reaction in message.reactions
            if str(reaction.emoji) == event.emoji_name
        ][0]
    ).count

    if num_reaction == min_reaction:
        await starboard.bot.rest.create_message(
            1035754257686728734, "this message has been starred."
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(starboard)
