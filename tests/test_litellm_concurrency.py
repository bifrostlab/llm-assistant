import asyncio
from llm_assistant.discord_bot.ai.qa import async_answer_question
import time


question = "Hello, how are you"


async def _concurrent_call(model, n):
  asyncMethod = []
  for q in [question for _ in range(n)]:
    asyncMethod.append(async_answer_question(model, q))

  out = await asyncio.gather(*asyncMethod)
  return sum([x[1] for x in out])


def test_concurrency():
  models = ["test"]
  for model in models:
    start = time.time()
    separate_time = asyncio.run(_concurrent_call(model, 3))
    concurrent_time = time.time() - start

    assert separate_time / 2 > concurrent_time
