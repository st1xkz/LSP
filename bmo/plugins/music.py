import hikari
import tanjun

from asyncio import sleep
from songbird import ytdl
from songbird.hikari import Voicebox

music = tanjun.Component(name="music")


@music.with_slash_command
@tanjun.with_str_slash_option("url", "the URL of the song")
@tanjun.as_slash_command("play", "Plays a song from URL")
async def cmd_play(ctx: tanjun.abc.Context, url: str) -> None:
    guild = ctx.get_guild()
    user_voice = guild.get_voice_state(ctx.user)
    vc = user_voice.channel_id
    voice = await Voicebox.connect(ctx.client, ctx.guild_id, vc)

    await ctx.respond("Connected!")
    track_handle = await voice.play_source(await ytdl(url))
    track_handle.play()


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(music.copy())
