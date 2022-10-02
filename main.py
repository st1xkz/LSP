import hikari

from bmo.client import build_bot

if __name__ == "__main__":
    build_bot().run(
        status=hikari.Status.ONLINE,
        activity=hikari.Activity(
            name=f"{len(app.cache.get_available_guilds_view())} guilds & {len(app.cache.get_users_view())} users!",
            type=hikari.ActivityType.WATCHING,
        ),
    )
