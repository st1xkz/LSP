import hikari
import tanjun

starboard = tanjun.Component()

emoji = "\u2b50"
min_reaction = 1  # Minimum reactions required to add the message to starboard


@starboard.with_listener(hikari.GuildReactionAddEvent)
async def on_reaction_create(event: hikari.GuildReactionAddEvent):
    # Make sure the bot is listening to events
    print(event.emoji_name)
    if event.app.is_alive:
        return
    if not str(event.emoji_name) == "\u2b50":
        return

    message = event.app.cache.get_message(
        event.message_id
    ) or await event.app.rest.fetch_message(event.guild_id, event.message_id)
    num_reaction = (
        [
            reaction
            for reaction in message.reactions
            if str(reaction.emoji) == event.emoji_name
        ][0]
    ).count

    if num_reaction == min_reaction:
        await event.app.rest.create_message(
            1035754257686728734, "this message has been starred."
        )


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(starboard.copy())
