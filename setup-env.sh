#!/bin/bash

# Install jupyter notebook in a new (virtual) environment.
pip install notebook
pip install jupyter_nbextensions_configurator
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install
jupyter nbextensions_configurator enable --user
