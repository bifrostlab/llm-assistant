import winston from 'winston';
import { isProduction } from './is-production';

const consoleTransport = new winston.transports.Console();

const devOptions: winston.LoggerOptions = {
  level: 'debug',
  defaultMeta: { service: 'llm-assistant-dev', timestamp: Date.now() },
  transports: [consoleTransport],
  format: winston.format.combine(winston.format.timestamp(), winston.format.prettyPrint({ colorize: true })),
};

const prodOptions: winston.LoggerOptions = {
  level: 'info',
  defaultMeta: { service: 'llm-assistant', timestamp: Date.now() },
  transports: [consoleTransport],
  format: winston.format.combine(winston.format.errors({ stack: true }), winston.format.json()),
};

export const logger = winston.createLogger(isProduction() ? prodOptions : devOptions);
