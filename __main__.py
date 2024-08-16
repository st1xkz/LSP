import hikari

from lsp.bot import bot

if __name__ == "__main__":
    bot.run(
        status=hikari.Status.IDLE,
        activity=hikari.Activity(name="Oh, my Glob!", type=hikari.ActivityType.PLAYING),
    )
