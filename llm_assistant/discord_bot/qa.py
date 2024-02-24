from openai import AsyncOpenAI

import time


async def answer_question(model: str, question: str, server_url: str):
  start = time.time()
  # We don't need an api_key here. See `./README.md`.
  client = AsyncOpenAI(base_url=server_url, api_key="dont_need_api_key_here")
  response = await client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": question}],
  )
  out = response.choices[0].message.content

  return out, time.time() - start
