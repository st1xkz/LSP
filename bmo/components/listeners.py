import hikari
import tanjun

listener = tanjun.Component(name="Listeners")


@listener.with_slash_command
@tanjun.as_slash_command("foo", "Bar")
async def cmd_foo(ctx: tanjun.abc.Context) -> None:
    ...


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(listener.copy())
