# Discord Bot

In `qa.py`, we modify OpenAI client to interact **our LiteLLM proxy server instead** by setting `base_url` to our LiteLLM URL. And, LiteLLM is using OpenAI API key from the environment variable to use OpenAI models (have a look at [litellm/README.md](../litellm/README.md)). 

So, we can use **any string value** for the OpenAI API key since it is not affecting anything.

Please visit [here (Section "Quick Start Proxy - CLI")](https://github.com/BerriAI/litellm) for more information.
