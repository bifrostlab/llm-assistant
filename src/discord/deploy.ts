import { REST, type RequestData, type RouteLike } from '@discordjs/rest';
import { Routes } from 'discord-api-types/v10';
import type { SlashCommand } from '../slash-commands/builder';

interface DiscordRequestConfig {
  token: string;
  clientId: string;
  guildId: string;
}

interface DiscordRequestPayload {
  request: RouteLike;
  token: DiscordRequestConfig['token'];
  body: RequestData['body'];
}

async function registerCommands({ request, token, body }: DiscordRequestPayload): Promise<unknown> {
  const rest = new REST({ version: '10' }).setToken(token);
  return rest.put(request, { body });
}

export async function deployGuildCommands(commandList: SlashCommand[], config: DiscordRequestConfig): Promise<unknown> {
  const { token, clientId, guildId } = config;

  const commands = commandList.map((cmd) => cmd.data.toJSON());

  const request = Routes.applicationGuildCommands(clientId, guildId);
  return registerCommands({ request, token, body: commands });
}

export async function deployGlobalCommands(commandList: SlashCommand[], config: Omit<DiscordRequestConfig, 'guildId'>): Promise<unknown> {
  const { token, clientId } = config;

  const commands = commandList.map((cmd) => cmd.data.toJSON());

  const request = Routes.applicationCommands(clientId);
  return registerCommands({ request, token, body: commands });
}
