import interactions
import re
import llm
from settings import Settings


MODEL_CHOICES = ["gpt-3.5-turbo", "gpt-4", "phi"]
DEFAULT_MODEL = MODEL_CHOICES[0]
DISCORD_BOT_TOKEN = Settings().DISCORD_BOT_TOKEN
AI_SERVER_URL = Settings().AI_SERVER_URL

bot = interactions.Client(intents=interactions.Intents.DEFAULT)


@interactions.listen()
async def on_ready() -> None:
  print("Ready")
  print(f"This bot is owned by {bot.owner}")


@interactions.listen()
async def on_message_create(event: interactions.api.events.MessageCreate) -> None:
  print(f"Message received: {event.message.content}")


@interactions.slash_command(name="ask", description="Ask an LLM to answer anything")
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
async def ask(ctx: interactions.SlashContext, model: str = "", prompt: str = "") -> None:
  if model not in MODEL_CHOICES:
    await ctx.send(f"Invalid model `{model}`. Please choose from `{MODEL_CHOICES}`.")
    return

  await ctx.defer()

  response = await llm.answer_question(model, prompt, AI_SERVER_URL)
  for r in response:
    await ctx.send(r)


@ask.autocomplete("model")
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


@interactions.slash_command(name="review-resume", description="Ask an LLM to review a resume")
@interactions.slash_option(
  name="url",
  description="A downloadable url of your resume",
  required=True,
  opt_type=interactions.OptionType.STRING,
)
async def review_resume(ctx: interactions.SlashContext, url: str = "") -> None:
  # validate url structure, must have leading "http" and a domain name (e.g. "example.com"=`\w+\.\w+`)
  if not re.search(r"http.+\w+\.\w+", url):
    await ctx.send("Invalid URL. Please provide a valid URL of your resume.")
    return

  await ctx.defer()

  response = await llm.review_resume(DEFAULT_MODEL, url, AI_SERVER_URL)
  for r in response:
    await ctx.send(r)


def main() -> None:
  bot.start(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
  main()
