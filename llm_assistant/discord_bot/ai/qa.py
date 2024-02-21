import os
import dotenv
from openai import OpenAI, AsyncOpenAI

import time

dotenv.load_dotenv()


async def async_answer_question(model, question):
  start = time.time()
  ai_server = os.environ.get("ai_server", "http://localhost:8000")
  client = AsyncOpenAI(base_url=ai_server, api_key="FAKE")
  response = await client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": question}],
  )
  out = response.choices[0].message.content

  return out, time.time() - start


def answer_question(model, question):
  ai_server = os.environ.get("ai_server", "http://localhost:8000")
  client = OpenAI(base_url=ai_server, api_key="FAKE")
  response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": question}],
  )
  out = response.choices[0].message.content

  return out


if __name__ == "__main__":
  print(answer_question("gpt-3.5-turbo", "Tell me about Melbourne"))
