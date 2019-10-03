#!/bin/bash
export FLASK_APP=./src/__init__.py
source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0 -p 5000