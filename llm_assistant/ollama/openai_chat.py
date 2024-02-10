from openai import OpenAI
import argparse
client = OpenAI(base_url="http://0.0.0.0:8000", api_key="anything")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model")
    args = parser.parse_args()

    response = client.chat.completions.create(model=args.model, messages = [
        {
            "role": "user",
            "content": "write a short poem"
        }
    ], stream=True)

    for chunk in response:
        # print(chunk)
        print(chunk.choices[0].delta.content, end="", flush=True)
