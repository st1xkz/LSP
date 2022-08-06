from asyncio import sleep

import hikari
import tanjun
from songbird import ytdl
from songbird.hikari import Voicebox

music = tanjun.Component(name="music")


@music.with_slash_command
@tanjun.with_str_slash_option("url", "the URL of the song")
@tanjun.as_slash_command("play", "Plays a song from URL")
async def cmd_play(ctx: tanjun.abc.Context, url: str) -> None:
    assert ctx.guild_id is not None

    guild = ctx.get_guild()
    voice_state = guild.get_voice_state(ctx.author)
    if not voice_state or not voice_state.channel_id:
        await ctx.respond("Please connect to a voice channel first.")
        return None
    voice = await Voicebox.connect(ctx.client, ctx.guild_id, vc)

    track_handle = await voice.play_source(await ytdl(url))
    track_handle.play()


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(music.copy())
