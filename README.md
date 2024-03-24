# Multifunctional LLM Assistant for Discord

This project is a multifunctional assistant bot for Discord. It is designed by VAIT to help our members with various tasks, such as testing LLM models and quickly review our members resume.

## How to Run this Bot

### Setting up the bot in Discord

- [Create a bot in discord](https://interactions-py.github.io/interactions.py/Guides/02%20Creating%20Your%20Bot/).
- Add that bot to your server server.
  - When making the invite through OAuth2 URL Generator, make sure to enable `bot` and `applications.commands` options.
  - Follow the [Invite your bot](https://interactions-py.github.io/interactions.py/Guides/02%20Creating%20Your%20Bot/) section for reference.
- Copy out `.env.example` into `.env`, and fill in the `DISCORD_BOT_TOKEN` and `DISCORD_GUILD_ID`.
- Now, run the bot code locally; alternatively, you can deploy the bot in a docker-compose environment. See the sister repository [deploy-llm-bot](https://github.com/bifrostlab/deploy-llm-bot) for more information.
