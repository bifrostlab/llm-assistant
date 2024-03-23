"""
Although this module uses `openai` package but we are routing it
through our LiteLLM proxy to interact with Ollama and OpenAI models
by modifying the `base_url`.
"""

import os
import openai
import time
import fitz
import gdown

MAX_CHARACTERS = 2000
QUESTION_CUT_OFF_LENGTH = 150
RESERVED_SPACE = 50  # for other additional strings. E.g. number `(1/4)`, `Q: `, `A: `, etc.


async def answer_question(model: str, question: str, server_url: str) -> list[str]:
  """
  Calls the LLM model with the specified question and server URL to get the answer.
  """
  try:
    messages = await _call_llm(model, question, server_url)
    return messages
  except Exception as e:
    return [str(e)]


async def review_resume(model: str, url: str, server_url: str) -> list[str]:
  try:
    output_path = download_pdf(url)
    text = parse_pdf(output_path)
    os.remove(output_path)

    question = (
      "You are a resume reviewer. Your tasks are:\n"
      + "- Show sentences with incorrect grammars, and suggest a way to correct them.\n"
      + "- Provide suggestions to improve the resume: \n\n"
      + f"{text}"
    )

    messages = await _call_llm(model, question, server_url, attach_question_to_message=False)
    return messages
  except Exception as e:
    return [str(e)]


def download_pdf(url: str) -> str:
  try:
    if not os.path.exists("cache"):
      os.mkdir("cache")

    output_path = f"cache/{time.time()}.pdf"
    gdown.download(url, output_path, fuzzy=True)

    return output_path

  except Exception as e:
    raise RuntimeError(f"Error in downloading PDF: {e}")


def parse_pdf(pdf_path: str) -> str:
  try:
    with fitz.open(pdf_path) as pdf:
      text_list = []
      for page in pdf:
        text_list.append(page.get_text())
      text = "\n\n".join(text_list)

    return text

  except Exception as e:
    raise RuntimeError(f"Error in parsing PDF: {e}")


async def _call_llm(model: str, question: str, server_url: str, attach_question_to_message: bool = True) -> list[str]:
  """
  Calls the Language Model (LLM) to generate a response based on the given question.

  Args:
  - model (str): The name of the language model to use.
  - question (str): The question to be passed to the language model.
  - server_url (str): The URL of the server hosting the language model.
  - attach_question (bool, optional): Whether to attach the question to the generated response. 
      Defaults to True.
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
    raise RuntimeError(f"Error in calling the LLM: {e}")


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
