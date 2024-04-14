import { setupServer } from 'msw/node';
import { handlers as pdfHandlers } from './handlers/pdf';

export const server = setupServer(...pdfHandlers);
