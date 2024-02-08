# README
## SET UP OLLAMA
Please visit [here](https://github.com/ollama/ollama.git) and follow their instruction to install ollama on your machine.

*Note*: After installing, you could run a small model (microsoft-phi2) for testing on your local machine

```
ollama run phi
```

## RUN OpenAI and Ollama using the same OpenAI API Schema

Run OpenAI ChatGPT using the following code

```
export OPENAI_API_KEY=[YOUR_KEY]
python llm_assistant/demo.py OPENAI gpt-3.5-turbo
```

Run Ollama Phi using the following code. 
```
python llm_assistant/demo.py OLLAMA ollama/phi
```