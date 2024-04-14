# Developers Guide

## Prerequisite

### To run the bot

- Node 20
  - Can be installed via [source](https://nodejs.org/en/download)
  - Or via [nvm](https://github.com/nvm-sh/nvm) / [fnm](https://github.com/Schniz/fnm)
- [PNPM 8](https://pnpm.io/installation)
  - Can be installed as a standalone
  - Or via NPM (recommended): `npm --global install pnpm`

### To run the local LLM server (optional)

- Python 3.12
- Poetry 3.9
- Ollama
- See [`litellm`](../litellm/README.md) for more information.

## Available scripts

These can be viewed at the `scripts` section in [`package.json`](../package.json). Can be grouped in a few categories:

### Dev scripts

```shell
pnpm run start              # Start the bot
pnpm run test               # Run unit tests
pnpm run test:watch         # Run unit tests in watch mode
pnpm run lint               # Run linting
pnpm run lint:fix           # Run linting and fix issues
pnpm run lint:fix:unsafe    # Run linting and fix issues, including unsafe fixes
pnpm run format             # Run formatting
pnpm run typecheck          # Run typechecking
pnpm run build              # Bundle TS => JS code
```

### Discord related commands

Details to run these scripts can be viewed at the [Deploying commands](#deploying-commands) section.

```shell
pnpm run deploy:command         # Deploy guild commands
pnpm run delete:command         # Delete guild commands
pnpm run delete:command-global  # Delete GLOBAL commands
```

## Deploying commands

- Make sure you have filled out your `GUILD_ID`, `TOKEN` and `CLIENT_ID` in the `.env` file.
- Add your commands into the `src/commands.ts` file like so.

```ts
// file: src/commands.ts
import yourCommand from './your-command';

export const commands = [yourCommand];
```

- Run the `deploy:command` command.

```shell
pnpm run deploy:command
```

- **IMPORTANT:** You should only deploy your commands **ONCE ONLY** after there is a change in command registration (adding a new command, editing options of an existing one). Running this too many times in a short period of time will cause Discord API to **lock your bot out**.

## Troubleshooting

- When deploy slash commands, if you got `Error: Cannot deploy commands`, it's normally because of your bot doesn't have permission to do so. You need to authorize your bot with scope: `bot` and `applications.commands` using `https://discord.com/api/oauth2/authorize?client_id=$CLIENT_ID&permissions=0&scope=bot%20applications.commands`

- Another reason might be because the bot authorisation failed. Please open the `.env` file and make sure your credentials are correct.
