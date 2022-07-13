import tanjun

component = tanjun.Component()

@component.with_slash_command
@tanjun.as_slash_command("id", "find out your id")
async def cmd_id(ctx: tanjun.abc.Context) -> None:
    await ctx.respond(f"Your user ID is {ctx.author.id}")

@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())