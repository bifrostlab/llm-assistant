import dotenv
import interactions
import os

from discord_bot import llm

dotenv.load_dotenv()

MODEL_CHOICES = ["gpt-3.5-turbo", "gpt-4", "phi"]
DEFAULT_MODEL = os.environ.get("LLM_DEFAULT_MODEL", "phi")
DISCORD_BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
AI_SERVER_URL = os.environ["AI_SERVER_URL"]

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
  name="prompt", description="Enter your prompt", required=True, opt_type=interactions.OptionType.STRING, min_length=10
)
@interactions.slash_option(
  name="model",
  description="Choose an LLM model",
  required=False,
  opt_type=interactions.OptionType.STRING,
  choices=[interactions.SlashCommandChoice(name=model, value=model) for model in MODEL_CHOICES],
)
async def ask(ctx: interactions.SlashContext, prompt: str = "", model: str = DEFAULT_MODEL) -> None:
  if model not in MODEL_CHOICES:
    await ctx.send(f"Invalid model `{model}`. Please choose from `{MODEL_CHOICES}`.")
    return

  await ctx.defer()

  response = await llm.answer_question(model, prompt, AI_SERVER_URL)
  for r in response:
    await ctx.send(r)


@interactions.slash_command(name="review-resume", description="Ask an LLM to review a resume")
@interactions.slash_option(
  name="url",
  description="A downloadable url of your resume",
  required=True,
  opt_type=interactions.OptionType.STRING,
)
async def review_resume(ctx: interactions.SlashContext, url: str = "") -> None:
  await ctx.defer()
  response = await llm.review_resume(DEFAULT_MODEL, url, AI_SERVER_URL)
  for r in response:
    await ctx.send(r)


def main() -> None:
  bot.start(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
  main()
