"""
Although this module uses `openai` package but we are routing it
through our LiteLLM proxy to interact with Ollama and OpenAI models
by modifying the `base_url`.
"""

import openai


async def answer_question(model: str, question: str, server_url: str) -> list[str]:
  try:
    client = openai.AsyncOpenAI(base_url=server_url, api_key="FAKE")
    response = await client.chat.completions.create(
      model=model,
      messages=[{"role": "user", "content": question}],
    )
    content = response.choices[0].message.content or "No response from the model. Please try again"
    sliced_content = split(content)
    return sliced_content

  except Exception as e:
    return split(f"Error: {e}")


def split(answer: str) -> list[str]:
  """
  Split the answer into a list of smaller strings so that
  each element is less than 2000 characters.
  Full sentences are preserved.
  """
  messages = []
  answer = answer.strip()

  while len(answer) > 2000:
    last_period = answer[:2000].rfind(".")
    if last_period == -1:
      last_period = answer[:2000].rfind(" ")
    messages.append(answer[: last_period + 1])
    answer = answer[last_period + 1 :]

  messages.append(answer)

  return messages

