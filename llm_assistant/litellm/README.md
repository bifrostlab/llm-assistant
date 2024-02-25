# README

## SET UP OLLAMA

Please visit [here](https://github.com/ollama/ollama.git) and follow their instruction to install ollama on your machine.

*Note*: After installing, you could run a small model (microsoft-phi2) for testing on your local machine

```shell
ollama run phi
```

## Use LiteLLM as a Proxy to re-use OpenAI interface to interact with both OpenAI and Ollama models  

Edit the proxy server config at `proxy_config.yaml`, add the desired models the the corresponding parameters. Please visit [here](https://docs.litellm.ai/docs/proxy/quick_start) for the available settings

Run the proxy server:

```shell
# if you use OpenAI models
export OPENAI_API_KEY=<your_key>
litellm --config llm_assistant/litellm/proxy_config.yaml
```

After starting the LiteLLM Proxy server, run these commands. You should receive a response from the bot:

```shell
python test_litellm_proxy.py gpt-3.5-turbo
python test_litellm_proxy.py phi
```
