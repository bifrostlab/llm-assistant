import os
import interactions
import dotenv
import llm

dotenv.load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
MODEL_CHOICES = ["gpt-3.5-turbo", "gpt-4", "phi"]
AI_SERVER_URL = os.getenv("AI_SERVER_URL")

bot = interactions.Client(intents=interactions.Intents.DEFAULT)


@interactions.listen()
async def on_ready() -> None:
  print("Ready")
  print(f"This bot is owned by {bot.owner}")


@interactions.listen()
async def on_message_create(event: interactions.api.events.MessageCreate) -> None:
  print(f"message received: {event.message.content}")


@interactions.slash_command(name="ask", description="Ask an LLM")
@interactions.slash_option(
  name="model",
  description="Choose an LLM model",
  required=True,
  opt_type=interactions.OptionType.STRING,
  autocomplete=True,
)
@interactions.slash_option(
  name="prompt", description="Enter your prompt", required=True, opt_type=interactions.OptionType.STRING, min_length=10
)
async def ask_model(ctx: interactions.SlashContext, model: str = "", prompt: str = "") -> None:
  if model not in MODEL_CHOICES:
    await ctx.send(f"Invalid model `{model}`. Please choose from `{MODEL_CHOICES}`.")
    return

  response = await llm.answer_question(model, prompt, AI_SERVER_URL)
  await ctx.send(response)


@ask_model.autocomplete("model")
async def autocomplete(ctx: interactions.AutocompleteContext) -> None:
  string_option_input = ctx.input_text
  # you can use ctx.kwargs.get("name") to get the current state of other options - note they can be empty too
  # make sure you respond within three seconds

  filtered_choices = [choice for choice in MODEL_CHOICES if string_option_input in choice]

  await ctx.send(
    choices=[
      {
        "name": choice,
        "value": choice,
      }
      for choice in filtered_choices
    ]
  )


if __name__ == "__main__":
  bot.start(DISCORD_BOT_TOKEN)
