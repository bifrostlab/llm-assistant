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
    content = split_answer(content)
    return content

  except Exception as e:
    return split_answer(f"Error: {e}")


def split_answer(answer: str) -> list[str]:
  '''
  Split the answer into a list of smaller strings so that
  each element is less than 2000 characters.
  '''
  return [answer[i:i + 2000] for i in range(0, len(answer), 2000)]
