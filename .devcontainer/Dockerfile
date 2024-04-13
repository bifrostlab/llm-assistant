FROM mcr.microsoft.com/devcontainers/typescript-node:20-bookworm
LABEL org.opencontainers.image.authors="https://github.com/nqngo,https://github.com/samhwang"
LABEL description="TypeScript NodeJS devcontainers with PNPM"

ARG packages="pnpm typescript"
RUN npm -g install ${packages} && \
    npm cache clean --force
