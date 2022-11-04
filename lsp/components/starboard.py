import hikari
import tanjun

starboard = tanjun.Component()


@starboard.with_listener(hikari.MemberCreateEvent)
async def on_reaction_create(event: hikari.MemberCreateEvent):
    ...


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(starboard.copy())
