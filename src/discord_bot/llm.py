"""
Although this module uses `openai` package but we are routing it
through our LiteLLM proxy to interact with Ollama and OpenAI models
by modifying the `base_url`.
"""

import os
import openai
import re
from utils import llm_response, pdf


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
    messages = llm_response.split(content)
    messages = llm_response.add_number(messages)
    if attach_question_to_message:
      messages = llm_response.add_question(messages, question)

    return messages

  except Exception as e:
    return llm_response.split(f"Error in calling the LLM: {e}")


async def review_resume(model: str, url: str, server_url: str) -> list[str]:
  # validate url structure, must have leading "http[s]?" and a domain name (e.g. "example.com"=`\w+\.\w+`)
  if not re.search(r"http[s]?://\w+\.\w+", url):
    return llm_response.split("Invalid URL. Please provide a valid URL of your resume.")

  output_path = ""
  try:
    output_path = pdf.download(url)
    if not pdf.validate_pdf_format(output_path):
      return llm_response.split("Error: Invalid PDF format. Please provide a valid PDF file.")
    text = pdf.parse_to_text(output_path)
  except Exception as e:
    return llm_response.split(f"Error in processing PDF: {e}")
  finally:
    if os.path.exists(output_path):
      os.remove(output_path)

  question = (
    "You are a resume reviewer. Your tasks are:\n"
    + "- Show sentences with incorrect grammars, and suggest a way to correct them.\n"
    + "- Provide suggestions to improve the resume: \n\n"
    + f"{text}"
  )

  messages = await answer_question(model, question, server_url, attach_question_to_message=False)
  return messages
