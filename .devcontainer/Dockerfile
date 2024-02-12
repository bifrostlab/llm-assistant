FROM mcr.microsoft.com/devcontainers/python:3.12
LABEL org.opencontainers.image.authors="https://github.com/nqngo"
LABEL description="Python 3.12 devcontainer with poetry"

# Configure the dev environment
RUN apt-get update && \
    apt-get install -y bash-completion && \
    rm -rf /var/lib/apt/list/*
# Configure poetry
RUN pipx install poetry && \
    poetry completions bash > /etc/bash_completion.d/poetry
