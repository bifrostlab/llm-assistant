import asyncio
import time
import typing
import dotenv
import pytest
from discord_bot import llm
from unittest.mock import patch


AI_SERVER_URL = "http://localhost:8000"
MODEL = "phi"
dotenv.load_dotenv()
simple_prompt = "Hello world!"


@pytest.mark.asyncio
async def test_answer_question__LLM_should_response() -> None:
  response = await llm.answer_question(MODEL, simple_prompt, AI_SERVER_URL)

  assert not response[0].startswith("Error")


@pytest.mark.asyncio
async def test_answer_concurrent_question__should_be_at_the_same_time() -> None:
  n_models = 2

  # Get the average time for generating a character in a single run
  start = time.time()
  out_single = await llm.answer_question(MODEL, simple_prompt, AI_SERVER_URL)
  average_single_time = (time.time() - start) / len(out_single)

  # Get the average time for generating a character when running n_models concurrently
  start = time.time()
  out_concurrent = await _concurrent_call(MODEL, n_models, simple_prompt, AI_SERVER_URL)
  average_concurrent_time = (time.time() - start) / sum([len(x) for x in out_concurrent])

  assert (
    average_concurrent_time < average_single_time * n_models
  ), f"Running {n_models} separately should take more time than running them concurrently"


async def _concurrent_call(model: str, n_models: int, prompt: str, server_url: str) -> list[str]:
  asyncMethod = []
  for _ in range(n_models):
    asyncMethod.append(llm.answer_question(model, prompt, server_url))

  out = await asyncio.gather(*asyncMethod)
  return out


@pytest.mark.asyncio
async def test_review_resume__valid_url() -> None:
  valid_urls = [
    "https://example.com",
    "http://example.com/my_resume",
    "https://drive.google.com/my_resume.pdf",
    "https://drive.google.com/file/d/R0KJKJKJKJJKJK-aaaaBbb/view?usp=sharing",
  ]

  for url in valid_urls:
    response = await llm.review_resume(MODEL, url, AI_SERVER_URL)
    assert not response[0].startswith("Error: Invalid URL")


@pytest.mark.asyncio
async def test_review_resume__invalid_url() -> None:
  invalid_urls = ["example.com", "https://example", "https://drive/my_resume.pdf", "some_link"]

  for url in invalid_urls:
    response = await llm.review_resume(MODEL, url, AI_SERVER_URL)
    assert response[0].startswith("Error: Invalid URL")


@pytest.mark.asyncio
@patch("discord_bot.llm.answer_question", return_value=["Mocked answer 1", "Mocked answer 2"])
async def test_review_resume__call_answer_question_once(mock_answer_question: typing.Any) -> None:
  url = "https://www.orimi.com/pdf-test.pdf"

  messages = await llm.review_resume(MODEL, url, AI_SERVER_URL)

  assert messages == ["Mocked answer 1", "Mocked answer 2"]
  mock_answer_question.assert_called_once()
