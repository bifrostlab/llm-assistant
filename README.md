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
- Create your own discord server, add that bot to a test server (feel free to use )
- Implement bot logics (and add bot token to your code too)
- Now, run the bot code locally and test the bot on your server

### Auto formatter for Python
We use [Ruff](https://github.com/astral-sh/ruff) for linting and code formating. Ruff is already included and installed when you use `poetry install`. Follow the [instructions here](https://github.com/astral-sh/ruff) to use Ruff.

**TL;DR:**  
Just use this (Lint all files in the current directory and any subdirectories) before committing new code.
```
ruff check .
``` 
