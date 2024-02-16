# Multifunctional LLM Assistant for Discord

## Dependencies Installation
We will use [Poetry](https://python-poetry.org/docs/) in this project. Please visit the link to install poetry on your local machine.

After successfully installing Poetry, use the following command to install the project dependencies:

```
poetry install
```

This command will create a Python virtual environment and install all the required dependencies into that environment.

To activate the Python environment, run:

```
poetry shell
```

When you’re done working in the virtual environment, simply type:

```
exit
```

## Discord Bot Development

### Getting started
- [Create a bot in discord](https://interactions-py.github.io/interactions.py/Guides/02%20Creating%20Your%20Bot/)
- Add that bot to a test server.
  - When making the invite through OAuth2 URL Generator, make sure to enable `bot` and `applications.commands` options.
  - Follow the [Invite your bot](https://interactions-py.github.io/interactions.py/Guides/02%20Creating%20Your%20Bot/) section for reference.
- Copy out `.env.example` into `.env`, and fill in the `DISCORD_BOT_TOKEN` and `DISCORD_GUILD_ID`
- Now, run the bot code locally and test the bot on your server