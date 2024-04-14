################
# Build assets #
################
FROM node:20.10 as build
WORKDIR /app

# Install global node modules: pnpm
RUN npm install -g pnpm@8.15

# Install Node modules
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile --ignore-scripts

COPY . .

ENV NODE_ENV=production
RUN pnpm build

####################
# Production image #
####################
FROM node:20.10-slim as production
WORKDIR /app

COPY --chown=node:node --from=build /app/dist dist

USER node
ENV NODE_ENV=production
CMD ["--enable-source-maps", "dist/index.js"]
