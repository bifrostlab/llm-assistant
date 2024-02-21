from openai import OpenAI
import argparse

# We don't need an actual api_key here. See `ollama/README.md`
client = OpenAI(base_url="http://localhost:8000", api_key="FAKE")

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
