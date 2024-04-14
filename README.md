# Multifunctional LLM Assistant for Discord

This project is a multifunctional assistant bot for Discord. It is designed by VAIT to help our members with various tasks, such as asking LLM models and quickly reviewing our members resume.

Project is bootstrapped with [ts-starter-template](https://github.com/samhwang/ts-starter-template)

## How to Run this Bot

### Setting up the bot in Discord

- [Create a bot in discord](https://interactions-py.github.io/interactions.py/Guides/02%20Creating%20Your%20Bot/).
- Add that bot to your server.
  - When making the invite through OAuth2 URL Generator, make sure to enable 
    - `bot` and `applications.commands` options
    - all `Privileged Gateway Intents` options
  - Follow the [Invite your bot](https://interactions-py.github.io/interactions.py/Guides/02%20Creating%20Your%20Bot/) section for reference.
- Copy out `.env.example` into `.env`, and fill in the environment variables.
- Now, run the bot code locally; alternatively, you can deploy the bot in a docker-compose environment. See the sister repository [deploy-llm-bot](https://github.com/bifrostlab/deploy-llm-bot) for more information.

## Prerequisite

### To run the bot

- Node 20
- PNPM 8

### To run the local LLM server (optional)

- Python 3.12
- Poetry 3.9
- Ollama

## Available scripts

```shell
pnpm run start
pnpm run test
pnpm run format
pnpm run build
```
