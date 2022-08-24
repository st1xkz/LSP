import tanjun

music = tanjun.Component(name="Music")


@music.with_slash_command
@tanjun.with_str_slash_option("url", "the URL of the song")
@tanjun.as_slash_command("play", "Plays a song from URL")
async def cmd_play(ctx: tanjun.abc.Context, url: str) -> None:
    pass

"""
    assert ctx.guild_id is not None

    guild = ctx.get_guild()
    voice_state = guild.get_voice_state(ctx.author)
    if not voice_state or not voice_state.channel_id:
        await ctx.respond("Please connect to a voice channel first.")
        return None
    voice = await Voicebox.connect(ctx.client, ctx.guild_id, voice_state.channel_id)

    await ctx.respond(
        f"👍 **Joined `{ctx.client.cache.get_guild_channel(voice_state.channel_id).name}`**"
    )
    track_handle = await voice.play_source(await ytdl(url))
    track_handle.play()

"""
@music.with_slash_command
@tanjun.as_slash_command("leave", "Leaves the connected voice channel")
async def cmd_leave(ctx: tanjun.abc.Context) -> None:
    assert ctx.guild_id is not None

    guild = ctx.get_guild()
    voice_state = guild.get_voice_state(ctx.author)
    if not voice_state or not voice_state.channel_id:
        await ctx.respond("I am not connected to a voice channel.")
        return None
    voice = await ctx.client.voice.disconnect(ctx.guild_id)

    await ctx.respond(
        f"👋 **Successfully disconnected from `{ctx.client.cache.get_guild_channel(voice_state.channel_id).name}`**"
    )
"""


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(music.copy())
