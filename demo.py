import os
import argparse
import dotenv
import litellm
import openai
from litellm import completion

from config import LLM_CONFIG

dotenv.load_dotenv()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model_type", default="OPENAI")
    parser.add_argument("model", default="gpt-3.5-turbo")
    args = parser.parse_args()

    api_base = LLM_CONFIG[args.model_type]["api_base"]

    model=args.model
    response = completion(
        model=model,
        messages=[{ "content": "respond in 20 words. who are you?","role": "user"}], 
        api_base=api_base,
        stream=True
    )
    print(response)
    for chunk in response:
        print(chunk['choices'][0]['delta'])