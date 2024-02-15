#!/bin/bash
poetry install
poetry shell
poetry run pre-commit install