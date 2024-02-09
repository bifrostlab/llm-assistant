import os
from dotenv import load_dotenv
import asyncio
from interactions import (
    AutocompleteContext,
    Client,
    Intents,
    listen,
    slash_command,
    SlashContext,
    SlashCommand,
    slash_option,
    SlashCommandChoice,
    OptionType,
)

vait_guild_id = [1230000000999]  # THIS SHOULD BE ASSIGNED to scopes WHEN DEPLOYED

bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine


@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@listen()
async def on_message_create(event):
    # This event is called when a message is sent in a channel the bot can see
    print(f"message received: {event.message.content}")


@slash_command(name="my_short_command", description="My first command :)")
async def my_short_command(ctx: SlashContext):
    await ctx.send("Hello World")


@slash_command(name="my_long_command", description="My second command :)")
async def my_long_command_function(ctx: SlashContext):
    # need to defer it, otherwise, it fails
    await ctx.defer()

    # do stuff for a bit
    await asyncio.sleep(600)

    await ctx.send("Hello World")


@slash_command(name="ask", description="Ask an LLM")
@slash_option(
    name="model",
    description="aaaaa",
    required=True,
    opt_type=OptionType.STRING,
    autocomplete=True,
    choices=[
        SlashCommandChoice(name="gpt3", value="gpt3"),
        SlashCommandChoice(name="gpt4", value="gpt4"),
        SlashCommandChoice(name="g", value="ggggg"),
    ],
)
async def ask_model(ctx: SlashContext, model: str):
    await ctx.send(f"You asked model {model}")


@ask_model.autocomplete("model")
async def autocomplete(ctx: AutocompleteContext):
    string_option_input = ctx.input_text  # can be empty
    print(f"input: {string_option_input}")

    # you can use ctx.kwargs.get("name") to get the current state of other options - note they can be empty too

    # make sure you respond within three seconds
    print(f"waiting...")
    await ctx.send(
        choices=[
            {
                "name": f"gpt3",
                "value": f"gpt3",
            },
            {
                "name": f"gpt4",
                "value": f"gpt4",
            },
            {
                "name": f"{string_option_input}a",
                "value": f"{string_option_input}a",
            },
            {
                "name": f"{string_option_input}b",
                "value": f"{string_option_input}b",
            },
            {
                "name": f"{string_option_input}c",
                "value": f"{string_option_input}c",
            },
        ]
    )


load_dotenv()
bot.start(os.getenv("DISCORD_BOT_TOKEN"))
