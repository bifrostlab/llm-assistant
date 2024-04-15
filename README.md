# Multifunctional LLM Assistant for Discord

This project is a multifunctional assistant bot for Discord. It is designed by VAIT to utilise LLMs to help our members with various tasks, such as answering questions and quickly reviewing our members' resumes.

Project is bootstrapped with [ts-starter-template](https://github.com/samhwang/ts-starter-template)

## How to Run this Bot

### Setting up the bot in Discord

- [Create a bot in discord](https://discordjs.guide/preparations/setting-up-a-bot-application.html#creating-your-bot).
- Add that bot to your server.
  - When making the invite through OAuth2 URL Generator, make sure to enable
    - `bot` and `applications.commands` options
    - `Privileged Gateway Intents => Message Content Intent` options
  - Follow the [Invite your bot](https://discordjs.guide/preparations/adding-your-bot-to-servers.html) section for reference.
- Copy out `.env.example` into `.env`, and fill in the environment variables.
  - `GUILD_ID`: Your server ID. Right-click on the server title and select "Copy ID" to get the `GUILD ID`. **Development purposes only.**
  - `TOKEN`: Your bot token. Taken from the Discord Developer Portal => Bot section.
  - `PUBLIC_KEY`: Your bot public key. Taken from the Discord Developer Portal => General Information section.
  - `CLIENT_ID`: Your bot client ID. Taken from the Discord Developer Portal => OAuth2 section.
  - `AI_SERVER_URL`: The URL of the LiteLLM Proxy server.
- Now, run the bot code locally; alternatively, you can deploy the bot in a docker-compose environment. See the sister repository [deploy-llm-bot](https://github.com/bifrostlab/deploy-llm-bot) for more information.

---

## Developers Guide

Go to [DEV_GUIDE.md](./.github/DEV_GUIDE.md) for more details.
