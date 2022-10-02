import hikari

from bmo.client import build_bot, make_client

if __name__ == "__main__":
    build_bot().run(
        status=hikari.Status.ONLINE,
        activity=hikari.Activity(
            name=f"{len(make_client.cache.get_available_guilds_view())} guilds & {len(make_client.cache.get_users_view())} users!",
            type=hikari.ActivityType.WATCHING,
        ),
    )
