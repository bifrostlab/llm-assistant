import { SlashCommandBuilder } from 'discord.js';
import { Result } from 'oxide.ts';
import { selectModelAutocomplete } from '../../autocompletes/select-model/autocomplete';
import { askQuestion, findModel } from '../../llm/utils';
import { logger } from '../../utils/logger';
import type { SlashCommand, SlashCommandHandler } from '../builder';

const data = new SlashCommandBuilder()
  .setName('ask')
  .setDescription('Ask an LLM to answer anything')
  .addStringOption((option) => option.setName('model').setDescription('Choose an LLM model').setRequired(true).setAutocomplete(true))
  .addStringOption((option) => option.setName('question').setDescription('Enter your prompt').setRequired(true).setMinLength(10));

export const execute: SlashCommandHandler = async (interaction) => {
  await interaction.deferReply();
  const model = interaction.options.getString('model', true).trim().toLowerCase();
  const question = interaction.options.getString('question', true).trim();
  logger.info(`[ask]: Asking ${model} model with prompt: ${question}`);

  const findModelOp = Result.safe(() => findModel(model));
  if (findModelOp.isErr()) {
    logger.info(`[ask]: Invalid model ${model}`);
    interaction.editReply('Invalid model. Please choose from the available models.');
    return;
  }
  const supportedModel = findModelOp.unwrap();

  logger.info(`[ask]: Asking LLM with prompt: ${question}`);
  const answers = await askQuestion(supportedModel, question);

  logger.info('[ask]: Got response from LLM. Sending to client.', answers);
  const [firstChunk, ...chunks] = answers;
  await interaction.editReply(firstChunk);
  for await (const chunk of chunks) {
    interaction.followUp(chunk);
  }
};

const command: SlashCommand = {
  data,
  execute,
  autocomplete: selectModelAutocomplete,
};

export default command;
