FROM mcr.microsoft.com/devcontainers/python:3.12
LABEL org.opencontainers.image.authors="https://github.com/nqngo"
LABEL description="Python 3.12 devcontainer with poetry"

# Configure the dev environment
RUN apt update && \
    apt install -y bash-completion && \
    rm -rf /var/lib/apt/list/*
# Configure poetry
USER vscode
WORKDIR /home/vscode
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    .local/bin/poetry completions bash | sudo tee -a /etc/bash_completion.d/poetry
