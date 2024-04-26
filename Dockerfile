################
# Build assets #
################
FROM node:20.12 as build
WORKDIR /app

# Install global node modules: pnpm
RUN npm install -g pnpm@9.0

# Install Node modules
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile --ignore-scripts

COPY . .

ENV NODE_ENV=production
RUN pnpm build && \
    pnpm install --production --frozen-lockfile --ignore-scripts

####################
# Production image #
####################
FROM node:20.12-slim as production
WORKDIR /app

COPY --chown=node:node --from=build /app/dist dist
COPY --chown=node:node --from=build /app/node_modules node_modules

USER node
ENV NODE_ENV=production
CMD ["--enable-source-maps", "dist/index.js"]
