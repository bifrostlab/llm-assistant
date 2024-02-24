# Discord Bot

In `qa.py`, we modify OpenAI client to interact **our LiteLLM proxy server instead**. Specifically, we set `base_url` to our LiteLLM URL. So, we can use **any string value** for the OpenAI API key. 

Please visit [here (Section "Quick Start Proxy - CLI")](https://github.com/BerriAI/litellm) for more information.
