import type { AutocompleteInteraction } from 'discord.js';

export type AutocompleteHandler = (autocomplete: AutocompleteInteraction) => Promise<void>;
