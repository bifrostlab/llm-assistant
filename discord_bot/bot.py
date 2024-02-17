import os
from dotenv import load_dotenv
import asyncio
import interactions

bot = interactions.Client(intents=interactions.Intents.DEFAULT)


@interactions.listen()
async def on_ready():
  print("Ready")
  print(f"This bot is owned by {bot.owner}")


@interactions.listen()
async def on_message_create(event):
  print(f"message received: {event.message.content}")


@interactions.slash_command(name="my_short_command", description="My first command :)")
async def my_short_command(ctx: interactions.SlashContext):
  await ctx.send("Hello World")


@interactions.slash_command(name="my_long_command", description="My second command :)")
async def my_long_command_function(ctx: interactions.SlashContext):
  await ctx.defer()  # use defer for time-comsuming commands
  await asyncio.sleep(600)
  await ctx.send("Hello World")


@interactions.slash_command(name="ask", description="Ask an LLM")
@interactions.slash_option(
  name="model",
  description="Choose an LLM model",
  required=True,
  opt_type=interactions.OptionType.STRING,
  autocomplete=True,
)
@interactions.slash_option(
  name="prompt",
  description="Enter your prompt",
  required=True,
  opt_type=interactions.OptionType.STRING
)
async def ask_model(ctx: interactions.SlashContext, model: str = "", prompt: str = ""):
  await ctx.send(f"You asked model {model} with the prompt: \"{prompt}\"")


@ask_model.autocomplete("model")
async def autocomplete(ctx: interactions.AutocompleteContext):
  string_option_input = ctx.input_text  # note: can be empty
  print(f"input: {string_option_input}")
  # you can use ctx.kwargs.get("name") to get the current state of other options - note they can be empty too
  # make sure you respond within three seconds

  choices = ["gpt3", "gpt4"]
  filtered_choices = [choice for choice in choices if string_option_input in choice]

  await ctx.send(
    choices=[
      {
        "name": choice,
        "value": choice,
      }
      for choice in filtered_choices
    ]
  )


load_dotenv()
bot.start(os.getenv("DISCORD_BOT_TOKEN"))
