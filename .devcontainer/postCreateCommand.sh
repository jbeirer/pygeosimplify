#! /usr/bin/env bash

# Install pyqt5
sudo apt-get update && sudo apt-get -y install python3-pyqt5

# Configure Poetry to create the virtual environment inside the project
poetry config virtualenvs.in-project true

# Install Dependencies
poetry install --with dev

# Install pre-commit hooks
poetry run pre-commit install --install-hooks
