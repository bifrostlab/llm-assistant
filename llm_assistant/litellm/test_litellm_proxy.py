import asyncio
import os
import openai
import argparse
import dotenv
import llm_assistant.discord_bot.qa

dotenv.load_dotenv()
AI_SERVER_URL = os.getenv("AI_SERVER_URL")


async def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("model")
  args = parser.parse_args()

  response, response_time = await llm_assistant.discord_bot.qa.answer_question(args.model, "write a short poem", AI_SERVER_URL)
  print(response)


if __name__ == "__main__":
  asyncio.run(main())
