import hikari
import tanjun

starboard = tanjun.Component()


@starboard.with_listener(hikari.ReactionAddEvent)
async def on_reaction_create(event: hikari.ReactionAddEvent):
    ...


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(starboard.copy())
