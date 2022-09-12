import tanjun

music = tanjun.Component(name="Music")


@music.with_slash_command
@tanjun.with_str_slash_option("url", "the URL of the song")
@tanjun.as_slash_command("play", "Plays a song from URL")
async def cmd_play(ctx: tanjun.abc.Context, url: str) -> None:
    ...


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(music.copy())
