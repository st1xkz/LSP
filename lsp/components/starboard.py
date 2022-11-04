import hikari
import tanjun

starboard = tanjun.Component()


@starboard.with_listener(hikari.ReactionCreateEvent)
async def on_reaction_create(event: hikari.ReactionCreateEvent):
    ...


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(starboard.copy())
