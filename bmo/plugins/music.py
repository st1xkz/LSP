import hikari
import tanjun

music = tanjun.Component(name="meta")


@music.with_slash_command
@tanjun.as_slash_command("play", "Plays a song")
async def cmd_play(ctx: tanjun.abc.Context) -> None:
    ...


@tanjun.is_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(music.copy())
