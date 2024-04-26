import type { ChatInputCommandInteraction, SlashCommandBuilder, SlashCommandSubcommandBuilder, SlashCommandSubcommandsOnlyBuilder } from 'discord.js';
import type { AutocompleteHandler } from '../autocompletes/builder';

export type SlashCommandHandler = (interaction: ChatInputCommandInteraction) => Promise<void>;

export type SlashCommand = {
  data: Omit<SlashCommandBuilder, 'addSubcommandGroup' | 'addSubcommand'> | SlashCommandSubcommandsOnlyBuilder;
  execute: SlashCommandHandler;
  autocomplete?: AutocompleteHandler;
};

export type Subcommand = {
  data: SlashCommandSubcommandBuilder | ((subcommandGroup: SlashCommandSubcommandBuilder) => SlashCommandSubcommandBuilder);
  execute: SlashCommandHandler;
};
