"""
Although this module uses `openai` package but we are routing it
through our LiteLLM proxy to interact with Ollama and OpenAI models 
by modifying the `base_url`.
"""

import openai


async def answer_question(model: str, question: str, server_url: str) -> str:
  client = openai.AsyncOpenAI(base_url=server_url, api_key="FAKE")
  response = await client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": question}],
  )

  out = response.choices[0].message.content or "No response from the model"

  return out
