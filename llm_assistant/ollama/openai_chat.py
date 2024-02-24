import os
from openai import OpenAI
import argparse
import dotenv
dotenv.load_dotenv()

# We don't need an actual api_key here. See `ollama/README.md`
ai_server_url = os.getenv("AI_SERVER_URL")
client = OpenAI(base_url=ai_server_url, api_key="dont_need_api_key_here")

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("model")
  args = parser.parse_args()

  response = client.chat.completions.create(
    model=args.model,
    messages=[{"role": "user", "content": "write a short poem"}],
    stream=True,
  )

  for chunk in response:
    # print(chunk)
    print(chunk.choices[0].delta.content, end="", flush=True)
