import type { AutocompleteInteraction } from 'discord.js';
import { beforeEach, describe, expect, it } from 'vitest';
import { captor, mockDeep, mockReset } from 'vitest-mock-extended';
import { selectModelAutocomplete } from './autocomplete';

const mockAutocompleteInteraction = mockDeep<AutocompleteInteraction>();

describe('autocomplete', () => {
  beforeEach(() => {
    mockReset(mockAutocompleteInteraction);
  });

  it('Should return nothing if no options are found', async () => {
    mockAutocompleteInteraction.options.getString.mockReturnValueOnce('some random search that not existed');
    const respondInput = captor<Parameters<AutocompleteInteraction['respond']>['0']>();

    await selectModelAutocomplete(mockAutocompleteInteraction);

    expect(mockAutocompleteInteraction.respond).toBeCalledWith(respondInput);
    expect(respondInput.value.length).toEqual(0);
  });

  it('Should return some options if search term is long enough and a result can be found', async () => {
    mockAutocompleteInteraction.options.getString.mockReturnValueOnce('phi');
    const respondInput = captor<Parameters<AutocompleteInteraction['respond']>['0']>();

    await selectModelAutocomplete(mockAutocompleteInteraction);

    expect(mockAutocompleteInteraction.respond).toBeCalledWith(respondInput);
    expect(respondInput.value).toMatchInlineSnapshot(`
    [
      {
        "name": "phi",
        "value": "phi",
      },
      {
        "name": "tinydolphin",
        "value": "tinydolphin",
      },
    ]
  `);
  });
});
