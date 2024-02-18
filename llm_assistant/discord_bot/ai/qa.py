import os
import dotenv
from openai import OpenAI


dotenv.load_dotenv()


async def async_answer_question(model, question):
  return answer_question(model, question)


def answer_question(model, question):
  ai_server = os.environ.get("ai_server", "http://0.0.0.0:8000")
  client = OpenAI(base_url=ai_server, api_key="FAKE")
  response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": question}],
  )

  return response.choices[0].message.content


if __name__ == "__main__":
  print(answer_question("gpt-3.5-turbo", "Tell me about Melbourne"))
