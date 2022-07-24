import hikari
import tanjun

errors = tanjun.AnyHooks()


@errors.with_on_error
async def on_error(ctx: tanjun.abc.Context, exc: Exception) -> None:
    users = ctx.cache.get_user(994738626816647262)
    await ctx.respond(
        f"Something went wrong during invocation of command `{ctx.command.name}`."
    )

    embed = hikari.Embed(
        title=f"An unexpected `{type(exc).__name__}` occurred",
        description=f"```py\n{str(exc)[:1950]}```",
    )
    await users.send(embed)


@errors.add_to_command
@tanjun.as_slash_command("name", "description")
async def slash_command(ctx: tanjun.abc.Context) -> None:
    ...
