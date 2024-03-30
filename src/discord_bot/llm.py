"""
Although this module uses `openai` package but we are routing it
through our LiteLLM proxy to interact with Ollama and OpenAI models
by modifying the `base_url`.
"""

import os
import openai
import utils.pdf

MAX_CHARACTERS = 2000
QUESTION_CUT_OFF_LENGTH = 150
RESERVED_SPACE = 50  # for other additional strings. E.g. number `(1/4)`, `Q: `, `A: `, etc.


async def answer_question(model: str, question: str, server_url: str, attach_question_to_message: bool = True) -> list[str]:
  """
  Calls the LLM model with the specified question and server URL to get the answer.
  """
  try:
    client = openai.AsyncOpenAI(base_url=server_url, api_key="FAKE")
    response = await client.chat.completions.create(
      model=model,
      messages=[{"role": "user", "content": question}],
    )
    content = response.choices[0].message.content or "No response from the model. Please try again"
    messages = split(content)
    messages = add_number(messages)
    if attach_question_to_message:
      messages = add_question(messages, question)

    return messages

  except Exception as e:
    return split(f"Error in calling the LLM: {e}")


async def review_resume(model: str, url: str, server_url: str) -> list[str]:
  try:
    output_path = utils.pdf.download_pdf(url)
    text = utils.pdf.parse_pdf(output_path)
    os.remove(output_path)
  except Exception as e:
    return split(f"Error in processing PDF: {e}")

  question = (
    "You are a resume reviewer. Your tasks are:\n"
    + "- Show sentences with incorrect grammars, and suggest a way to correct them.\n"
    + "- Provide suggestions to improve the resume: \n\n"
    + f"{text}"
  )

  messages = await answer_question(model, question, server_url, attach_question_to_message=False)
  return messages


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
