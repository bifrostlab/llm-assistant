import asyncio
import time
import dotenv
import pytest
from typing import List
from discord_bot.llm import answer_question

AI_SERVER_URL = "http://localhost:8000"
dotenv.load_dotenv()


@pytest.mark.asyncio
async def test_answer_question__LLM_should_response() -> None:
  model = "tinydolphin"
  prompt = "Respond shortly: hello!"

  response = await answer_question(model, prompt, AI_SERVER_URL)

  assert not response.startswith("Error")


@pytest.mark.asyncio
async def test_answer_question__invalid_model() -> None:
  model = "not-a-gpt"
  prompt = "Hello, world!"

  response = await answer_question(model, prompt, AI_SERVER_URL)

  assert response.startswith("Error")


@pytest.mark.asyncio
async def test_answer_concurrent_question__should_be_at_the_same_time() -> None:
  model = "tinydolphin"
  prompt = "Respond shortly: hello"
  n_models = 2

  # Get the average time for generating a character in a single run
  start = time.time()
  out_single = await answer_question(model, prompt, AI_SERVER_URL)
  average_single_time = (time.time() - start) / len(out_single)

  # Get the average time for generating a character when running n_models concurrently
  start = time.time()
  out_concurrent = await _concurrent_call(model, n_models, prompt, AI_SERVER_URL)
  average_concurrent_time = (time.time() - start) / sum([len(x) for x in out_concurrent])

  assert (
    average_concurrent_time < average_single_time * n_models
  ), f"Running {n_models} separately should take more time than running them concurrently"


async def _concurrent_call(model: str, n_models: int, prompt: str, server_url: str) -> List[str]:
  asyncMethod = []
  for _ in range(n_models):
    asyncMethod.append(answer_question(model, prompt, server_url))

  out = await asyncio.gather(*asyncMethod)
  return out
