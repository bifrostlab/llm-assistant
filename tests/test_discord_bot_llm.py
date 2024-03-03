import os
import dotenv
import pytest
import src.discord_bot.llm

AI_SERVER_URL = os.getenv("AI_SERVER_URL") or "http://localhost:8000"
dotenv.load_dotenv()


@pytest.mark.asyncio
async def test_answer_question__LLM_should_response() -> None:
  model = "gpt-3.5-turbo"
  prompt = "reply me with exactly 123hi and 123hi only, no capitalised letters"

  response = await src.discord_bot.llm.answer_question(model, prompt, AI_SERVER_URL)

  assert response == "123hi"


@pytest.mark.asyncio
async def test_answer_question__invalid_server_url() -> None:
  model = "gpt-3.5-turbo"
  prompt = "Hello, world!"

  response = await src.discord_bot.llm.answer_question(model, prompt, "http://fakeurl.com")

  assert response.startswith("Error")


@pytest.mark.asyncio
async def test_answer_question__invalid_model() -> None:
  model = "not-a-gpt"
  prompt = "Hello, world!"

  response = await src.discord_bot.llm.answer_question(model, prompt, AI_SERVER_URL)

  assert response.startswith("Error")
