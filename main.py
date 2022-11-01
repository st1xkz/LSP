import hikari

from lsp.client import build_bot

if __name__ == "__main__":
    build_bot().run(
        status=hikari.Status.IDLE,
        activity=hikari.Activity(name="oh, my glob!", type=hikari.ActivityType.PLAYING),
    )
