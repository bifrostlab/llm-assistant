from openai import AsyncOpenAI


async def answer_question(model: str, question: str, server_url: str):
  # We don't need an api_key here. See `./README.md`.
  client = AsyncOpenAI(base_url=server_url, api_key="FAKE")
  response = await client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": question}],
  )
  out = response.choices[0].message.content

  return out
