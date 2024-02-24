import os
import dotenv
from openai import AsyncOpenAI

import time

dotenv.load_dotenv()


async def async_answer_question(model, question):
  start = time.time()
  ai_server_url = os.getenv("AI_SERVER_URL")
  client = AsyncOpenAI(base_url=ai_server_url, api_key="FAKE")
  response = await client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": question}],
  )
  out = response.choices[0].message.content

  return out, time.time() - start
