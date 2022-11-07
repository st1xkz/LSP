from traceback import format_exception

import hikari
import tanjun

errors = lightbulb.Plugin()


@errors_plugin.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    users = [
        ctx.cache.get_user(user) for user in [690631795473121280, 994738626816647262]
    ]  # 1: main, 2: second
    await ctx.respond(
        f"Something went wrong during invocation of command `{ctx.command.name}`."
    )

    for user in users:
        assert user
        await user.send(
            embed=hikari.Embed(
                title=f"An unexpected `{type(exc).__name__}` occurred",
                description=f"```py\n{''.join(format_exception(exc.__class__, exc, exc.__traceback__))}```",
            )
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(errors)
