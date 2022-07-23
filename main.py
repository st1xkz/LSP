import hikari

from bmo.client import build_bot

if __name__ == "__main__":
    build_bot().run(
        status=hikari.Status.ONLINE,
        activity=hikari.Activity(
            name="I think I am dying. But that's okay, BMO always bounces back!",
            type=hikari.ActivityType.PLAYING,
        ),
    )