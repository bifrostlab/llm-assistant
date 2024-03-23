"""
Although this module uses `openai` package but we are routing it
through our LiteLLM proxy to interact with Ollama and OpenAI models
by modifying the `base_url`.
"""

import os
import openai
import time
import fitz

MAX_CHARACTERS = 2000
QUESTION_CUT_OFF_LENGTH = 150
RESERVED_SPACE = 50  # for other additional strings. E.g. number `(1/4)`, `Q: `, `A: `, etc.


async def _call_llm(model: str, question: str, server_url: str, is_add_question: bool = True) -> list[str]:
  try:
    client = openai.AsyncOpenAI(base_url=server_url, api_key="FAKE")
    response = await client.chat.completions.create(
      model=model,
      messages=[{"role": "user", "content": question}],
    )
    content = response.choices[0].message.content or "No response from the model. Please try again"
    messages = split(content)
    messages = add_number(messages)
    if is_add_question:
      messages = add_question(messages, question)

    return messages

  except Exception as e:
    return split(f"Error: {e}")


async def review_resume(model: str, url: str, server_url: str) -> list[str]:
  try:
    # Download PDF
    if not os.path.exists("cache"):
      os.mkdir("cache")

    output_path = f"cache/{time.time()}.pdf"
    os.system(f"poetry run gdown -O {output_path} --fuzzy {url}")
    ## Some how calling gdown inside this function lead to 100% memory utilization
    # gdown.download(url, output_path, fuzzy=True)

    # Parse PDF
    downloaded_file = fitz.open(output_path)
    text_list = []
    for page in downloaded_file:
      text_list.append(page.get_text())
    text = "\n\n".join(text_list)
    os.remove(output_path)  # Remove the downloaded file

    print(f"Parsed content: {text}")

    question = f"You are a resume reviewer. Your tasks are:\n- Show sentences with incorrect grammars, and suggest a way to correct them.\n- Provide suggestions to improve the resume: \n\n{text}"

    return await _call_llm(model, question, server_url, is_add_question=False)
  except Exception as e:
    return split(f"Error: {e}")


async def answer_question(model: str, question: str, server_url: str) -> list[str]:
  return await _call_llm(model, question, server_url, is_add_question=True)


def split(answer: str) -> list[str]:
  """
  Split the answer into a list of smaller strings so that
  each element is less than MAX_CHARACTERS characters.
  Full sentences are preserved.
  """
  limit = MAX_CHARACTERS - RESERVED_SPACE - QUESTION_CUT_OFF_LENGTH
  messages = []
  answer = answer.strip()

  while len(answer) > limit:
    last_period = answer[:limit].rfind(".")
    if last_period == -1:
      last_period = answer[:limit].rfind(" ")
    messages.append(answer[: last_period + 1])
    answer = answer[last_period + 1 :]

  messages.append(answer)

  return messages


def add_question(messages: list[str], questions: str) -> list[str]:
  """
  Add the asked question to the beginning of each message.
  """
  return [(f"Q: {questions[:QUESTION_CUT_OFF_LENGTH]}\n" + f"A: {message}") for message in messages]


def add_number(messages: list[str]) -> list[str]:
  """
  Add the number to the beginning of each message. E.g. `(1/4)`
  Do nothing if the length of `messages` is 1.
  """
  if len(messages) == 1:
    return messages

  for i, message in enumerate(messages):
    message = message.strip()
    messages[i] = f"({i+1}/{len(messages)}) {message}"

  return messages
