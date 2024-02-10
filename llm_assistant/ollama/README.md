# README
## SET UP OLLAMA
Please visit [here](https://github.com/ollama/ollama.git) and follow their instruction to install ollama on your machine.

*Note*: After installing, you could run a small model (microsoft-phi2) for testing on your local machine

```
ollama run phi
```


## Use LiteLLM as a Proxy to re-use OpenAI interface to interact with both OpenAI models and Ollama

Edit the proxy server config at `proxy_config.yaml`, add the desired models the the corresponding parameters. Please visit [here](https://docs.litellm.ai/docs/proxy/quick_start) for the available settings 

Run the proxy server
```
# if you use OpenAI models
export OPENAI_API_KEY=<your_key> 
litellm --config llm_assistant/ollama/proxy_config.yaml
```


Modify OpenAI SDK to interact with our proxy server instead
```
python openai_chat.py gpt-3.5-turbo
python openai_chat.py phi
```


