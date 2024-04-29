import { SUPPORTED_MODELS_MAP } from '../../llm/utils';
import type { AutocompleteHandler } from '../builder';

function get25ptions(models: typeof SUPPORTED_MODELS_MAP) {
  return models.slice(0, 25);
}

export const selectModelAutocomplete: AutocompleteHandler = async (interaction) => {
  let searchTerm = interaction.options.getString('model', false);
  if (!searchTerm) {
    const options = get25ptions(SUPPORTED_MODELS_MAP);
    interaction.respond(options);
    return;
  }

  searchTerm = searchTerm.trim().toLowerCase();
  const filtered = SUPPORTED_MODELS_MAP.filter((model) => model.name.includes(searchTerm));
  const options = get25ptions(filtered);
  interaction.respond(options);
};
