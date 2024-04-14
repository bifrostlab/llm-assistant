import { SUPPORTED_MODELS_MAP } from '../../llm/utils';
import type { AutocompleteHandler } from '../builder';

export const selectModelAutocomplete: AutocompleteHandler = async (interaction) => {
  const searchTerm = interaction.options.getString('model', true).trim().toLowerCase();

  const options = SUPPORTED_MODELS_MAP.filter((model) => {
    if (!searchTerm) return true;
    return model.name.includes(searchTerm);
  }).slice(0, 25);
  interaction.respond(options);
};
