import tanjun
import typing

errors = tanjun.AnyHooks()


@errors.with_on_error
async def on_error(ctx: tanjun.abc.Context, exc: Exception) -> typing.Optional[bool]:
    await ctx.respond(f"Something went wrong during invocation of command `{ctx.command.name}`.")


@errors.add_to_command
@tanjun.as_slash_command("name", "description")
async def slash_command(ctx: tanjun.abc.Context) -> None:
    ...