# README

## SET UP OLLAMA

Please visit [here](https://github.com/ollama/ollama.git) and follow their instruction to install ollama on your machine.

*Note*: After installing, you could run a small model (microsoft-phi2) for testing on your local machine

```shell
ollama run phi
```

## Use LiteLLM as a Proxy to re-use OpenAI interface to interact with both OpenAI models and Ollama

Edit the proxy server config at `proxy_config.yaml`, add the desired models the the corresponding parameters. Please visit [here](https://docs.litellm.ai/docs/proxy/quick_start) for the available settings

Run the proxy server:

```shell
# if you use OpenAI models
export OPENAI_API_KEY=<your_key>
litellm --config llm_assistant/ollama/proxy_config.yaml
```

*Note*: In `test_litellm_proxy` we use OpenAI API SDK to interact with proxy server. Although the SDK require to have an api key, we **don't need to include it here**. We can use **any string value** for the api key. This is because we are interacting with the proxy server, not the OpenAI server. Please visit [LiteLLM Docs](https://github.com/BerriAI/litellm), Section "Quick Start Proxy - CLI" for more information.

After starting the LiteLLM Proxy server, run these commands. You should receive a response from the bot:

```shell
python playgrounds/litellm_proxy.py gpt-3.5-turbo
python playgrounds/litellm_proxy.py phi
```
